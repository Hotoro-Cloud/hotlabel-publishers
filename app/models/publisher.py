from sqlalchemy import Boolean, Column, String, DateTime, JSON
from sqlalchemy.sql import func
import secrets
import uuid

from app.core.database import Base

class Publisher(Base):
    __tablename__ = "publishers"

    id = Column(String, primary_key=True, index=True, default=lambda: f"pub_{uuid.uuid4().hex[:8]}")
    name = Column(String, index=True)
    website = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    description = Column(String)
    
    # API access
    api_key = Column(String, unique=True, index=True, default=lambda: f"pk_live_{secrets.token_urlsafe(16)}")
    
    # Configuration
    configuration = Column(JSON, default=dict)
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
