from pydantic import BaseModel, EmailStr, HttpUrl, validator, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import re

class PublisherBase(BaseModel):
    company_name: str
    website_url: HttpUrl
    contact_email: EmailStr
    contact_name: str
    website_categories: List[str]
    estimated_monthly_traffic: int
    integration_platform: str
    preferred_task_types: List[str]

class PublisherCreate(PublisherBase):
    pass

class PublisherInDB(PublisherBase):
    id: str
    api_key: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    configuration: Dict[str, Any] = {}

    class Config:
        orm_mode = True

class Publisher(PublisherInDB):
    pass

class PublisherUpdate(BaseModel):
    company_name: Optional[str] = None
    website_url: Optional[HttpUrl] = None
    contact_email: Optional[EmailStr] = None
    contact_name: Optional[str] = None
    website_categories: Optional[List[str]] = None
    estimated_monthly_traffic: Optional[int] = None
    integration_platform: Optional[str] = None
    preferred_task_types: Optional[List[str]] = None
    is_active: Optional[bool] = None

class PublisherConfigurationUpdate(BaseModel):
    appearance: Optional[Dict[str, Any]] = None
    behavior: Optional[Dict[str, Any]] = None
    task_preferences: Optional[Dict[str, Any]] = None
    rewards: Optional[Dict[str, Any]] = None

class PublisherStatisticsParams(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    granularity: Optional[str] = "daily"

    @validator("granularity")
    def validate_granularity(cls, v):
        allowed_values = ["hourly", "daily", "weekly", "monthly"]
        if v not in allowed_values:
            raise ValueError(f"granularity must be one of {allowed_values}")
        return v

class IntegrationCodeParams(BaseModel):
    platform: Optional[str] = "custom"
    include_comments: Optional[bool] = True

    @validator("platform")
    def validate_platform(cls, v):
        allowed_values = ["wordpress", "custom", "react", "shopify", "wix"]
        if v not in allowed_values:
            raise ValueError(f"platform must be one of {allowed_values}")
        return v

class WebhookCreate(BaseModel):
    endpoint_url: HttpUrl
    secret_key: str
    events: List[str]
    active: bool = True

    @validator("events")
    def validate_events(cls, v):
        allowed_events = [
            "task.completed", 
            "user.session.expired",
            "quality.threshold.reached",
            "revenue.milestone.achieved"
        ]
        for event in v:
            if event not in allowed_events:
                raise ValueError(f"'{event}' is not a valid event. Must be one of {allowed_events}")
        return v

    @validator("secret_key")
    def validate_secret_key(cls, v):
        if not re.match(r'^whsec_[a-zA-Z0-9]{16,}$', v):
            raise ValueError("secret_key must be in format 'whsec_' followed by at least 16 alphanumeric characters")
        return v
