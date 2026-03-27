from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    created_at: datetime | None = None
    last_active_at: datetime | None = None


class EntityType(BaseModel):
    id: int
    slug: str
    display_name: str
    command: str
    points: int
    contact_required: bool
    congratulation_texts: list[str]
    sort_order: int
    created_at: datetime | None = None


class Entry(BaseModel):
    id: int
    user_id: int
    entity_type_id: int
    contact_username: str | None = None
    created_at: datetime | None = None


class ActivityLog(BaseModel):
    id: int
    user_id: int
    action: str
    metadata: dict | None = None
    created_at: datetime | None = None
