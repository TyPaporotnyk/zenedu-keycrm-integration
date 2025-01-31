from dataclasses import dataclass, field


@dataclass
class Pipeline:
    id: int
    name: str


@dataclass
class Client:
    id: int | None = field(default=None, kw_only=True)
    phones: list[str] = field(default_factory=list, kw_only=True)
    username: str | None = field(default=None, kw_only=True)
    manager_id: int = field(default=1, kw_only=True)
    full_name: str


@dataclass
class Lead:
    id: int | None = field(default=None, kw_only=True)
    manager_id: int = field(default=1, kw_only=True)
    client_id: int | None
    pipeline_id: int


@dataclass
class Integration:
    id: int
    bot_id: int
    pipeline_id: int
    is_active: bool
