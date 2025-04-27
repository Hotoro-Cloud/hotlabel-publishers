from pydantic import BaseModel
from typing import Dict, Any, List
from datetime import datetime

class Task(BaseModel):
    id: str
    title: str
    description: str
    content: Dict[str, Any]
    options: List[Dict[str, Any]]
    status: str
    created_at: datetime
    updated_at: datetime | None = None 