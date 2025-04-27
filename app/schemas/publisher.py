from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class PublisherBase(BaseModel):
    name: str
    email: EmailStr
    website: str
    description: str

class PublisherCreate(PublisherBase):
    pass

class PublisherUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    description: Optional[str] = None
    configuration: Optional[dict] = None

class PublisherInDB(PublisherBase):
    id: str
    api_key: str
    configuration: dict = {}
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class Publisher(PublisherInDB):
    pass

class PublisherConfigurationUpdate(BaseModel):
    appearance: dict | None = None
    behavior: dict | None = None
    task_preferences: dict | None = None
    rewards: dict | None = None
