from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime
from uuid import UUID

class Task(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None
    provider_id: UUID
    task_type: str
    content: Dict[str, Any]
    language: str = "en"
    category: Optional[str] = None
    complexity_level: Optional[int] = None
    options: Optional[Dict[str, Any]] = None
    time_estimate_seconds: Optional[int] = None
    tags: Optional[List[str]] = None
    golden_set: Optional[bool] = False
    created_at: datetime
    updated_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    status: str
    batch_id: Optional[UUID] = None
    result: Optional[Dict[str, Any]] = None
    quality_score: Optional[float] = None
    rejection_reason: Optional[str] = None

    class Config:
        from_attributes = True

class TaskListResponse(BaseModel):
    total: int
    items: List[Task]

    class Config:
        from_attributes = True 