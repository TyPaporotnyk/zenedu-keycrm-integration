from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Pipeline:
    id: int
    name: str


@dataclass
class Client:
    id: Optional[int] = field(default=None, kw_only=True)
    phone: Optional[str] = field(default=None, kw_only=True)
    username: Optional[str] = field(default=None, kw_only=True)
    email: Optional[str] = field(default=None, kw_only=True)
    manager_id: int = field(default=1, kw_only=True)
    full_name: str


@dataclass
class Lead:
    id: int | None = field(default=None, kw_only=True)
    title: str
    manager_id: int = field(default=1, kw_only=True)
    client_id: int | None
    pipeline_id: int
    source_id: int | None = field(default=2, kw_only=True)
    bot: str | None = field(default=None, kw_only=True)
    price: int | None = field(default=None, kw_only=True)
    currency: str | None = field(default=None, kw_only=True)
    status: str | None = field(default=None, kw_only=True)
    payment_methhod: str | None = field(default=None, kw_only=True)


@dataclass
class Integration:
    id: int
    bot_id: int
    pipeline_id: int
    is_active: bool


@dataclass
class Payment:
    amount: float
    status: str
    description: str
    payment_date: datetime
    # transaction_uuid: str
    payment_method_id: int = 6
    payment_method: str = "WayForPay"
