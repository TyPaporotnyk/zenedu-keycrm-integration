from dataclasses import dataclass

from django.utils.dateparse import parse_datetime
from httpx import Client

from apps.zenedu.entities import Bot, Subscriber


@dataclass
class ZeneduClient:
    http_client: Client
    api_key: str

    def _get_header(self) -> dict:
        return {"Accept": "application/json", "Authorization": f"Bearer {self.api_key}"}

    def get_all_bots(self) -> list[Bot]:
        response = self.http_client.get("api/v1/bots", headers=self._get_header())

        response.raise_for_status()

        data = response.json()
        bots = data["data"]

        return [
            Bot(
                id=bot["id"],
                name=bot["name"],
                username=bot["username"],
                is_active=bot["is_active"],
                created_at=parse_datetime(bot["created_at"]),
            )
            for bot in bots
        ]

    def get_all_customers_by_bot_id(self, bot_id: int, per_page=30, page=1) -> list[Subscriber]:
        params = {"per_page": per_page, "page": page}
        response = self.http_client.get(
            f"api/v1/bot/{bot_id}/subscribers",
            headers=self._get_header(),
            params=params,
        )

        response.raise_for_status()

        data = response.json()
        subscribers = data["data"]

        return [
            Subscriber(
                id=subscriber["id"],
                first_name=subscriber["first_name"],
                last_name=subscriber["last_name"],
                username=subscriber["username"],
                phone=subscriber["phone"],
                created_at=parse_datetime(subscriber["created_at"]),
            )
            for subscriber in subscribers
        ]
