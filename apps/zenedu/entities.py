from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Bot:
    id: int
    name: str
    username: str
    is_active: bool
    created_at: datetime


@dataclass
class Subscriber:
    id: int
    source_id: int | None = field(default=None, kw_only=True)
    first_name: str | None
    last_name: str | None
    username: str | None
    phone: str | None
    created_at: datetime

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


@dataclass
class Order:
    source_id: int
    price: float
    currency: str
    status: str
    payment_system_type: str
    subscriber: "Subscriber"
    created_at: datetime
    bot: Bot | None = None
    id: int | None = None
