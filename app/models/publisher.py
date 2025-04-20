from sqlalchemy import Boolean, Column, String, Integer, DateTime, JSON, Text
from sqlalchemy.sql import func
import secrets
import uuid

from app.core.database import Base

class Publisher(Base):
    __tablename__ = "publishers"

    id = Column(String, primary_key=True, index=True, default=lambda: f"pub_{uuid.uuid4().hex[:8]}")
    company_name = Column(String, index=True)
    website_url = Column(String, index=True)
    contact_email = Column(String, unique=True, index=True)
    contact_name = Column(String)
    website_categories = Column(JSON)
    estimated_monthly_traffic = Column(Integer)
    integration_platform = Column(String)
    preferred_task_types = Column(JSON)
    
    # API access
    api_key = Column(String, unique=True, index=True, default=lambda: f"pk_live_{secrets.token_urlsafe(16)}")
    
    # Configuration
    configuration = Column(JSON, default=dict)
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
