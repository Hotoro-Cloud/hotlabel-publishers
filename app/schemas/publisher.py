from typing import List, Optional
from pydantic import BaseModel, EmailStr, UUID4
from datetime import datetime

class PublisherBase(BaseModel):
    name: str
    email: EmailStr
    website: str
    description: str
    preferred_task_types: List[str] = []

class PublisherCreate(PublisherBase):
    pass

class PublisherUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    description: Optional[str] = None
    configuration: Optional[dict] = None
    preferred_task_types: Optional[List[str]] = None

class PublisherInDB(PublisherBase):
    id: UUID4
    api_key: str
    configuration: dict = {}
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class Publisher(PublisherInDB):
    pass

class PublisherResponse(PublisherInDB):
    pass

class PublisherConfigurationUpdate(BaseModel):
    appearance: dict | None = None
    behavior: dict | None = None
    task_preferences: dict | None = None
    rewards: dict | None = None
