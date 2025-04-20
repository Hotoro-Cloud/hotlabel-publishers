from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
import uuid
import secrets

from app.models.publisher import Publisher
from app.schemas.publisher import PublisherCreate, PublisherUpdate, PublisherConfigurationUpdate

def get_publisher(db: Session, publisher_id: str) -> Optional[Publisher]:
    return db.query(Publisher).filter(Publisher.id == publisher_id).first()

def get_publisher_by_email(db: Session, email: str) -> Optional[Publisher]:
    return db.query(Publisher).filter(Publisher.contact_email == email).first()

def get_publisher_by_api_key(db: Session, api_key: str) -> Optional[Publisher]:
    return db.query(Publisher).filter(Publisher.api_key == api_key).first()

def get_publishers(db: Session, skip: int = 0, limit: int = 100) -> List[Publisher]:
    return db.query(Publisher).offset(skip).limit(limit).all()

def create_publisher(db: Session, publisher: PublisherCreate) -> Publisher:
    # Generate unique ID and API key
    publisher_id = f"pub_{uuid.uuid4().hex[:8]}"
    api_key = f"pk_live_{secrets.token_urlsafe(16)}"
    
    # Create new publisher with default configuration
    db_publisher = Publisher(
        id=publisher_id,
        api_key=api_key,
        **publisher.dict(),
        configuration={
            "appearance": {
                "theme": "light",
                "primary_color": "#3366FF",
                "border_radius": "4px",
                "font_family": "Roboto, Arial, sans-serif"
            },
            "behavior": {
                "task_display_frequency": 300,
                "max_tasks_per_session": 5,
                "show_task_after_seconds": 30,
                "display_on_page_types": ["article", "video"]
            },
            "task_preferences": {
                "preferred_task_types": publisher.preferred_task_types,
                "max_complexity_level": 3,
                "preferred_languages": ["en"]
            },
            "rewards": {
                "content_access_duration_seconds": 3600,
                "show_completion_feedback": True
            }
        }
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
