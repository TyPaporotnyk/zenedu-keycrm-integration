from dataclasses import dataclass

from httpx import Client, HTTPStatusError

from apps.common.utils import rate_limit
from apps.keycrm import entities


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
            pipeline_id=data["pipeline_id"],
            manager_id=data["manager_id"],
            client_id=data["contact"]["client_id"],
            source_id=data["source_id"],
        )

    @rate_limit(key_prefix="keycrm-client-rate-limit")
    def create_lead(self, lead: entities.Lead) -> entities.Lead:
        json_data = {
            "manager_id": lead.manager_id,
            "pipeline_id": lead.pipeline_id,
            "source_id": lead.source_id,
            "contact": {"client_id": lead.client_id},
        }

        response = self.http_client.post("/pipelines/cards", headers=self._get_header(), json=json_data)

        response.raise_for_status()

        data = response.json()

        return entities.Lead(
            id=data["id"],
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
            phones=data["phone"],
        )

    @rate_limit(key_prefix="keycrm-client-rate-limit")
    def create_client(self, client: entities.Client) -> entities.Client:
        fields_mapping = {
            "full_name": client.full_name,
            "custom_fields": ([{"uuid": "CT_1015", "value": client.username}] if client.username else None),
            "phone": client.phones if client.phones else None,
        }

        json_data = {key: value for key, value in fields_mapping.items() if value is not None}

        response = self.http_client.post("/buyer", headers=self._get_header(), json=json_data)

        response.raise_for_status()
        data = response.json()

        return entities.Client(
            id=data["id"],
            full_name=data["full_name"],
            phones=data["phone"],
        )

    @rate_limit(key_prefix="keycrm-client-rate-limit")
    def update_client(self, client: entities.Client) -> entities.Client:
        fields_mapping = {
            "full_name": client.full_name,
            "custom_fields": ([{"uuid": "CT_1015", "value": client.username}] if client.username else None),
            "phone": client.phones if client.phones else None,
        }

        json_data = {key: value for key, value in fields_mapping.items() if value is not None}

        response = self.http_client.put(f"/buyer/{client.id}", headers=self._get_header(), json=json_data)

        response.raise_for_status()
        data = response.json()

        return entities.Client(
            id=data["id"],
            full_name=data["full_name"],
            phones=data["phone"],
        )
