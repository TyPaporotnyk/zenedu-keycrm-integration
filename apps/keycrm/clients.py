import logging
from dataclasses import dataclass

from httpx import Client, HTTPStatusError

from apps.common.utils import rate_limit
from apps.keycrm import entities

logger = logging.getLogger(__name__)


@dataclass
class KeyCRMClient:
    http_client: Client
    api_key: str

    def _get_header(self) -> dict:
        return {"Accept": "application/json", "Authorization": f"Bearer {self.api_key}"}

    @rate_limit(key_prefix="keycrm-client-rate-limit")
    def get_all_pipelines(self, limit=50, page=1) -> list[entities.Pipeline]:
        params = {"limit": limit, "page": page}
        response = self.http_client.get(
            "/pipelines",
            headers=self._get_header(),
            params=params,
        )

        response.raise_for_status()

        data = response.json()
        pipelines = data["data"]

        return [entities.Pipeline(id=pipeline["id"], name=pipeline["title"]) for pipeline in pipelines]

    @rate_limit(key_prefix="keycrm-client-rate-limit")
    def add_payment_to_lead(self, lead_id: int, payment: entities.Payment):
        json_data = {
            "payment_method_id": payment.payment_method_id,
            "payment_method": payment.payment_method,
            "amount": payment.amount,
            "status": payment.status,
            "description": payment.description,
            "payment_date": payment.payment_date.strftime("%Y-%m-%d %H:%M:%S"),
            "transaction_uuid": payment.transaction_uuid,
        }
        response = self.http_client.post(
            f"/pipelines/cards/{lead_id}/payment", headers=self._get_header(), json=json_data
        )

        response.raise_for_status()

    @rate_limit(key_prefix="keycrm-client-rate-limit")
    def get_lead_by_id(self, lead_id: int) -> entities.Lead:
        params = {"include": "contact.client"}
        response = self.http_client.get(f"/pipelines/cards/{lead_id}", headers=self._get_header(), params=params)

        try:
            response.raise_for_status()
        except HTTPStatusError as e:
            if response.status_code == 404:
                return None
            else:
                raise e

        data = response.json()

        return entities.Lead(
            id=data["id"],
            title=data["title"],
            pipeline_id=data["pipeline_id"],
            manager_id=data["manager_id"],
            client_id=data["contact"]["client_id"],
            source_id=data["source_id"],
        )

    @rate_limit(key_prefix="keycrm-client-rate-limit")
    def create_lead(self, lead: entities.Lead) -> entities.Lead:
        custom_fields = [
            {"uuid": "LD_1016", "value": lead.bot} if lead.bot else None,
        ]
        json_data = {
            "title": lead.title,
            "manager_id": lead.manager_id,
            "pipeline_id": lead.pipeline_id,
            "source_id": lead.source_id,
            "contact": {"client_id": lead.client_id},
            "custom_fields": [field for field in custom_fields if field],
        }

        response = self.http_client.post("/pipelines/cards", headers=self._get_header(), json=json_data)

        response.raise_for_status()

        data = response.json()

        return entities.Lead(
            id=data["id"],
            title=data["title"],
            pipeline_id=data["pipeline_id"],
            manager_id=data["manager_id"],
            client_id=data["contact"]["client_id"],
        )

    @rate_limit(key_prefix="keycrm-client-rate-limit")
    def get_client_by_id(self, client_id: int) -> entities.Client | None:
        params = {"include": "custom_fields"}
        response = self.http_client.get(f"/buyer/{client_id}", headers=self._get_header(), params=params)

        try:
            response.raise_for_status()
        except HTTPStatusError as e:
            if response.status_code == 404:
                return None
            else:
                raise e

        data = response.json()

        return entities.Client(
            id=data["id"],
            full_name=data["full_name"],
        )

    @rate_limit(key_prefix="keycrm-client-rate-limit")
    def create_client(self, client: entities.Client) -> entities.Client:
        custom_fields = [
            {"uuid": "CT_1015", "value": client.username} if client.username else None,
            {"uuid": "CT_1020", "value": client.phone} if client.phone else None,
        ]

        json_data = {
            "full_name": client.full_name,
            "custom_fields": [field for field in custom_fields if field],
        }

        response = self.http_client.post("/buyer", headers=self._get_header(), json=json_data)

        response.raise_for_status()
        data = response.json()

        return entities.Client(
            id=data["id"],
            full_name=data["full_name"],
            phone=data["phone"],
        )

    @rate_limit(key_prefix="keycrm-client-rate-limit")
    def update_client(self, client: entities.Client) -> entities.Client:
        custom_fields = [
            {"uuid": "CT_1015", "value": client.username} if client.username else None,
            {"uuid": "CT_1020", "value": client.phone} if client.phone else None,
        ]

        json_data = {
            "full_name": client.full_name,
            "custom_fields": [field for field in custom_fields if field],
        }

        response = self.http_client.put(f"/buyer/{client.id}", headers=self._get_header(), json=json_data)

        response.raise_for_status()
        data = response.json()

        return entities.Client(
            id=data["id"],
            full_name=data["full_name"],
            phone=data["phone"],
        )
