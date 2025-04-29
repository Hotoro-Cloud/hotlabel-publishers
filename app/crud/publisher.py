from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
import uuid
import secrets
import httpx
from fastapi import HTTPException, status
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.publisher import Publisher
from app.schemas.publisher import PublisherCreate, PublisherUpdate, PublisherConfigurationUpdate
from app.schemas.task import Task
from app.core.exceptions import ResourceNotFound, DuplicateResource
from app.core.config import settings

logger = logging.getLogger(__name__)

def get_publisher(db: Session, publisher_id: str) -> Optional[Publisher]:
    """
    Get a publisher by ID using synchronous SQLAlchemy session.
    
    Args:
        db: SQLAlchemy database session
        publisher_id: The publisher's UUID as a string
        
    Returns:
        Publisher object if found, None otherwise
    """
    try:
        # Convert string to UUID if needed
        if isinstance(publisher_id, str):
            try:
                publisher_id = uuid.UUID(publisher_id)
            except ValueError:
                # If it's not a valid UUID string, just continue with the original value
                pass
                
        return db.query(Publisher).filter(Publisher.id == publisher_id).first()
    except Exception as e:
        logger.error(f"Error in get_publisher: {str(e)}")
        return None

def get_publisher_by_email(db: Session, email: str) -> Optional[Publisher]:
    return db.query(Publisher).filter(Publisher.email == email).first()

def get_publisher_by_api_key(db: Session, api_key: str) -> Optional[Publisher]:
    return db.query(Publisher).filter(Publisher.api_key == api_key).first()

def get_publishers(db: Session, skip: int = 0, limit: int = 100) -> List[Publisher]:
    return db.query(Publisher).offset(skip).limit(limit).all()

def create_publisher(db: Session, publisher: PublisherCreate) -> Publisher:
    """
    Create a new publisher using synchronous SQLAlchemy session.
    Use this for synchronous route handlers.
    """
    # Check if publisher with same email exists
    existing = db.query(Publisher).filter(Publisher.email == publisher.email).first()
    if existing:
        raise DuplicateResource(f"Publisher with email {publisher.email} already exists")
    
    # Generate API key
    api_key = f"pk_live_{secrets.token_urlsafe(16)}"
    
    # Create new publisher
    db_publisher = Publisher(
        name=publisher.name,
        website=str(publisher.website),
        email=publisher.email,
        description=publisher.description,
        api_key=api_key
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

async def get_available_tasks(publisher_id: str, db: AsyncSession) -> List[Dict]:
    """Get available tasks for a publisher."""
    try:
        headers = {
            "X-Internal-Key": settings.SECRET_KEY,
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.TASKS_SERVICE_URL}/available",
                params={"publisher_id": str(publisher_id)},
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("items", [])
            else:
                logger.error(f"Failed to get available tasks: {response.text}")
                return []
                
    except Exception as e:
        logger.error(f"Error getting available tasks: {str(e)}")
        return []

def update_task_status(
    db: Session,
    task_id: str,
    status: str,
    result: Optional[Dict[str, Any]] = None,
    quality_score: Optional[float] = None,
    rejection_reason: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update the status of a task using the tasks service.
    
    Args:
        db: Database session
        task_id: ID of the task to update
        status: New status for the task
        result: Optional result data to submit
        quality_score: Optional quality score for the task
        rejection_reason: Optional reason for rejection
        
    Returns:
        Updated task data from the tasks service
        
    Raises:
        HTTPException: If the request to tasks service fails
    """
    try:
        # Prepare request data
        data = {
            "status": status
        }
        
        if result is not None:
            data["result"] = result
            
        if quality_score is not None:
            data["quality_score"] = quality_score
            
        if rejection_reason is not None:
            data["rejection_reason"] = rejection_reason
            
        # Make request to tasks service (internal communication)
        with httpx.Client() as client:
            # Use the internal service URL for service-to-service communication
            response = client.post(
                f"{settings.TASKS_SERVICE_URL}/api/v1/tasks/{task_id}/status",
                json=data,
                headers={"X-Internal-Service": "true"},
                timeout=10.0
            )
        
        # Handle response
        if response.status_code == status.HTTP_200_OK:
            return response.json()
        else:
            logger.error(f"Tasks service error: {response.status_code} - {response.text}")
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Error updating task status: {response.text}"
            )
            
    except httpx.RequestError as e:
        logger.error(f"Failed to connect to tasks service: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Tasks service is unavailable"
        )
    except Exception as e:
        logger.error(f"Unexpected error updating task status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while updating task status"
        )

async def async_get_publisher(db: AsyncSession, publisher_id: str) -> Optional[Publisher]:
    """Get a publisher by ID - async version."""
    result = await db.execute(select(Publisher).filter(Publisher.id == publisher_id))
    return result.scalar_one_or_none()

async def async_get_publisher_by_api_key(db: AsyncSession, api_key: str) -> Optional[Publisher]:
    """Get a publisher by API key - async version."""
    result = await db.execute(select(Publisher).filter(Publisher.api_key == api_key))
    return result.scalar_one_or_none()

async def async_create_publisher(db: AsyncSession, publisher: PublisherCreate) -> Publisher:
    """
    Create a new publisher using async SQLAlchemy session.
    Use this for asynchronous route handlers only.
    """
    # Generate API key
    api_key = f"pk_live_{secrets.token_urlsafe(16)}"
    
    db_publisher = Publisher(
        name=publisher.name,
        website=str(publisher.website),
        email=publisher.email,
        description=publisher.description,
        api_key=api_key
    )
    db.add(db_publisher)
    await db.commit()
    await db.refresh(db_publisher)
    return db_publisher

async def async_update_publisher(
    db: AsyncSession,
    db_obj: Publisher,
    obj_in: PublisherUpdate
) -> Publisher:
    """Update a publisher - async version."""
    update_data = obj_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj
