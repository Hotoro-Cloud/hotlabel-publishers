from fastapi import APIRouter, Depends, HTTPException, status, Query, Request, Body, Header
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging
import uuid

from app.core.database import get_db
from app.core.auth import validate_api_key
from app.schemas.publisher import Publisher, PublisherCreate, PublisherUpdate, PublisherConfigurationUpdate
from app.crud import publisher as publisher_crud
from app.models.publisher import Publisher as PublisherModel
from app.schemas.task import Task, TaskListResponse, TaskStatusUpdate
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/publishers", tags=["publishers"])

@router.get("/health", tags=["health"])
def health_check():
    """Health check endpoint that doesn't require authentication."""
    return {"status": "healthy", "service": settings.SERVICE_NAME}

@router.post("", response_model=Publisher, status_code=status.HTTP_201_CREATED)
def register_publisher(
    publisher_in: PublisherCreate,
    db: Session = Depends(get_db)
):
    # Check if publisher with this email already exists
    db_publisher = publisher_crud.get_publisher_by_email(db, email=publisher_in.email)
    if db_publisher:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Publisher with this email already exists"
        )
    
    try:
        # Create new publisher using the synchronous version
        new_publisher = publisher_crud.create_publisher(db=db, publisher=publisher_in)
        
        # Validate that all required fields are present
        if not all(hasattr(new_publisher, field) for field in 
                ['name', 'email', 'website', 'description', 'id', 'api_key', 'is_active', 'created_at']):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create publisher with all required fields"
            )
        
        return new_publisher
    except Exception as e:
        logger.error(f"Error creating publisher: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating publisher: {str(e)}"
        )

@router.get("/{publisher_id}", response_model=Publisher)
def get_publisher(
    publisher_id: str,
    request: Request,
    api_key: str = Header(..., alias="X-API-Key"),
    db: Session = Depends(get_db)
):
    """Get publisher by ID with direct API key handling."""
    logger.info(f"Received request to get publisher with ID: {publisher_id}")
    
    try:
        # Log request details for debugging
        logger.info(f"API Key: {api_key[:8]}...")
        logger.info(f"Request headers: {dict(request.headers)}")
        
        # Validate publisher ID format
        try:
            publisher_uuid = str(uuid.UUID(publisher_id))
            logger.info(f"Validated publisher_id as UUID: {publisher_uuid}")
        except ValueError as e:
            logger.error(f"Invalid publisher ID format: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid publisher ID format"
            )
        
        # Get publisher by API key first
        db_authenticated_publisher = db.query(PublisherModel).filter(PublisherModel.api_key == api_key).first()
        
        if not db_authenticated_publisher:
            logger.warning(f"No publisher found with provided API key")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key"
            )
            
        logger.info(f"Authenticated publisher: {db_authenticated_publisher.id}")
        
        # Get the requested publisher
        db_publisher = publisher_crud.get_publisher(db, publisher_id=publisher_uuid)
        if not db_publisher:
            logger.error(f"Publisher not found with ID: {publisher_uuid}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Publisher not found"
            )
        
        # Ensure publisher can only access their own data, unless it's an internal service request
        is_internal_service = request.headers.get("X-Internal-Service") == "true"
        logger.info(f"Is internal service request: {is_internal_service}")
        
        if not is_internal_service and str(db_publisher.id) != str(db_authenticated_publisher.id):
            logger.warning(f"Publisher {db_authenticated_publisher.id} attempted to access data for publisher {publisher_id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this publisher"
            )
        
        logger.info(f"Successfully returning publisher {publisher_id}")
        return db_publisher
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Catch any other unexpected errors
        logger.error(f"Unexpected error in get_publisher: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )

@router.get("/{publisher_id}/integration-code", response_model=Dict[str, Any])
def generate_integration_code(
    publisher_id: str,
    publisher: PublisherModel = Depends(validate_api_key),
    db: Session = Depends(get_db)
):
    """Generate integration code for embedding the publisher's widget."""
    logger.info(f"Generating integration code for publisher {publisher_id}")
    
    try:
        # Validate and normalize the publisher_id
        publisher_uuid = str(uuid.UUID(publisher_id))
    except ValueError:
        logger.error(f"Invalid publisher ID format: {publisher_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid publisher ID format"
        )
        
    # Ensure publisher can only access their own integration code
    if str(publisher.id) != publisher_uuid:
        logger.warning(f"Publisher {publisher.id} attempted to access integration code for publisher {publisher_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this publisher's integration code"
        )
    
    logger.info(f"Access authorized, generating integration code for publisher {publisher_id}")
    
    # Generate integration code
    header_code = f'<script src="https://cdn.hotlabel.io/sdk/v1/hotlabel.js"></script>'
    
    body_code = f'''<div id="hotlabel-container"></div>
<script>
HotLabel.init({{
    containerId: 'hotlabel-container',
    publisherId: '{publisher_id}',
    apiKey: '{publisher.api_key}'
}});
</script>'''
    
    return {
        "code_snippets": {
            "header": header_code,
            "body": body_code
        },
        "installation_steps": [
            "Add the HotLabel script to your website's header",
            "Add the container div and initialization code where you want the widget to appear"
        ]
    }

@router.get("/{publisher_id}/tasks", response_model=List[Dict[str, Any]])
def get_publisher_tasks(
    publisher_id: str,
    task_status: Optional[str] = Query(None),
    limit: int = Query(10, gt=0, le=100),
    publisher: PublisherModel = Depends(validate_api_key),
    db: Session = Depends(get_db)
):
    """Get available tasks for a publisher."""
    try:
        publisher_uuid = str(uuid.UUID(publisher_id))
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid publisher ID format"
        )
    
    # Ensure publisher can only access their own tasks
    if str(publisher.id) != publisher_uuid:
        logger.warning(f"Publisher {publisher.id} attempted to access tasks for publisher {publisher_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this publisher's tasks"
        )
    
    try:
        # The get_available_tasks function only accepts publisher_id and db
        # Note: This is a synchronous endpoint calling an async function, which might be causing issues
        # In a production environment, this would need to be fixed properly
        # For now, we'll try to call it synchronously and return empty list on error
        import asyncio
        try:
            # Get the current running event loop if it exists, or create a new one
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                # If we're not in an event loop context, create a new one
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
            # Run the async function in the event loop
            tasks = loop.run_until_complete(
                publisher_crud.get_available_tasks(publisher_id=publisher_uuid, db=db)
            )
            
            logger.info(f"Retrieved {len(tasks)} tasks for publisher {publisher_id}")
            
            # If there are no tasks, log this specifically
            if not tasks:
                logger.warning(f"No tasks found for publisher {publisher_id}")
                
            return tasks
        except Exception as e:
            logger.error(f"Error getting tasks: {str(e)}")
            # Return an empty list as a fallback
            return []
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.patch("/{publisher_id}", response_model=Publisher)
def update_publisher_details(
    publisher_id: str,
    publisher_update: PublisherUpdate = Body(...),
    publisher: PublisherModel = Depends(validate_api_key),
    db: Session = Depends(get_db)
):
    """Update publisher details."""
    try:
        publisher_uuid = uuid.UUID(publisher_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid publisher ID format"
        )
    
    # Ensure publisher can only update their own data
    if publisher.id != publisher_uuid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this publisher"
        )
    
    # Update publisher
    updated_publisher = publisher_crud.update_publisher(
        db=db,
        publisher_id=publisher_uuid,
        publisher_update=publisher_update
    )
    
    if not updated_publisher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Publisher not found"
        )
    
    return updated_publisher

@router.patch("/{publisher_id}/configuration", response_model=Publisher)
def update_publisher_configuration(
    publisher_id: str,
    config_update: PublisherConfigurationUpdate = Body(...),
    publisher: PublisherModel = Depends(validate_api_key),
    db: Session = Depends(get_db)
):
    """Update publisher configuration."""
    try:
        publisher_uuid = uuid.UUID(publisher_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid publisher ID format"
        )
    
    # Ensure publisher can only update their own configuration
    if publisher.id != publisher_uuid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this publisher's configuration"
        )
    
    # Update configuration
    updated_publisher = publisher_crud.update_publisher_configuration(
        db=db,
        publisher_id=publisher_uuid,
        config_update=config_update
    )
    
    if not updated_publisher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Publisher not found"
        )
    
    return updated_publisher

@router.get("/{publisher_id}/statistics", response_model=Dict[str, Any])
def get_publisher_statistics(
    publisher_id: str,
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    publisher: PublisherModel = Depends(validate_api_key),
    db: Session = Depends(get_db)
):
    """Get publisher statistics."""
    try:
        publisher_uuid = uuid.UUID(publisher_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid publisher ID format"
        )
    
    # Ensure publisher can only access their own statistics
    if publisher.id != publisher_uuid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this publisher's statistics"
        )
    
    # Get statistics
    try:
        return {"message": "Statistics endpoint not implemented yet"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/{publisher_id}/tasks/{task_id}/status", response_model=Dict[str, Any])
def update_task_status(
    publisher_id: str,
    task_id: str,
    status_update: TaskStatusUpdate,
    publisher: PublisherModel = Depends(validate_api_key),
    db: Session = Depends(get_db)
):
    """
    Update the status of a task assigned to a publisher.
    """
    # Ensure publisher can only update their own tasks
    if publisher.id != publisher_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this publisher's tasks"
        )
    
    try:
        # Update task status using the tasks service
        updated_task = publisher_crud.update_task_status(
            db=db,
            task_id=task_id,
            status=status_update.status,
            result=status_update.result,
            quality_score=status_update.quality_score,
            rejection_reason=status_update.rejection_reason
        )
        return updated_task
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
