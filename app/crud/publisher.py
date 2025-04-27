from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
import uuid
import secrets
import httpx

from app.models.publisher import Publisher
from app.schemas.publisher import PublisherCreate, PublisherUpdate, PublisherConfigurationUpdate
from app.schemas.task import Task
from app.core.exceptions import ResourceNotFound, DuplicateResource
from app.core.config import settings

def get_publisher(db: Session, publisher_id: str) -> Optional[Publisher]:
    return db.query(Publisher).filter(Publisher.id == publisher_id).first()

def get_publisher_by_email(db: Session, email: str) -> Optional[Publisher]:
    return db.query(Publisher).filter(Publisher.email == email).first()

def get_publisher_by_api_key(db: Session, api_key: str) -> Optional[Publisher]:
    return db.query(Publisher).filter(Publisher.api_key == api_key).first()

def get_publishers(db: Session, skip: int = 0, limit: int = 100) -> List[Publisher]:
    return db.query(Publisher).offset(skip).limit(limit).all()

def create_publisher(db: Session, publisher: PublisherCreate) -> Publisher:
    # Check if publisher with same email exists
    existing = db.query(Publisher).filter(Publisher.email == publisher.email).first()
    if existing:
        raise DuplicateResource(f"Publisher with email {publisher.email} already exists")
    
    # Create new publisher
    db_publisher = Publisher(
        name=publisher.name,
        website=str(publisher.website),
        email=publisher.email,
        description=publisher.description
    )
    db.add(db_publisher)
    db.commit()
    db.refresh(db_publisher)
    return db_publisher

def update_publisher(db: Session, publisher_id: str, publisher_update: PublisherUpdate) -> Optional[Publisher]:
    db_publisher = get_publisher(db, publisher_id)
    if not db_publisher:
        return None
    
    update_data = publisher_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_publisher, field, value)
    
    db.commit()
    db.refresh(db_publisher)
    return db_publisher

def update_publisher_configuration(
    db: Session, 
    publisher_id: str, 
    config_update: PublisherConfigurationUpdate
) -> Optional[Publisher]:
    db_publisher = get_publisher(db, publisher_id)
    if not db_publisher:
        return None
    
    # Get current configuration
    current_config = db_publisher.configuration or {}
    
    # Update configuration with new values
    config_update_dict = config_update.dict(exclude_unset=True)
    for section, section_data in config_update_dict.items():
        if section_data is not None:
            if section not in current_config:
                current_config[section] = {}
            current_config[section].update(section_data)
    
    # Save updated configuration
    db_publisher.configuration = current_config
    db.commit()
    db.refresh(db_publisher)
    return db_publisher

def regenerate_api_key(db: Session, publisher_id: str) -> Optional[str]:
    db_publisher = get_publisher(db, publisher_id)
    if not db_publisher:
        return None
    
    # Generate new API key
    new_api_key = f"pk_live_{secrets.token_urlsafe(16)}"
    db_publisher.api_key = new_api_key
    
    db.commit()
    return new_api_key

async def get_available_tasks(
    db: Session,
    publisher_id: str,
    status: Optional[str] = None,
    limit: int = 10
) -> List[Task]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.TASKS_SERVICE_URL}/api/v1/tasks",
            params={
                "provider_id": publisher_id,
                "status": status,
                "limit": limit
            }
        )
        if response.status_code == 200:
            tasks_data = response.json()
            if isinstance(tasks_data, dict) and "items" in tasks_data:
                return [Task(**task) for task in tasks_data["items"]]
            elif isinstance(tasks_data, list):
                return [Task(**task) for task in tasks_data]
            return []
        return []
