from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.auth import validate_api_key
from app.schemas.publisher import Publisher, PublisherCreate, PublisherUpdate, PublisherConfigurationUpdate
from app.crud import publisher as publisher_crud
from app.models.publisher import Publisher as PublisherModel
from app.schemas.task import Task, TaskListResponse

router = APIRouter(prefix="/publishers", tags=["publishers"])

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
    
    # Create new publisher
    return publisher_crud.create_publisher(db=db, publisher=publisher_in)

@router.get("/{publisher_id}", response_model=Publisher)
def get_publisher(
    publisher_id: str,
    publisher: PublisherModel = Depends(validate_api_key),
    db: Session = Depends(get_db)
):
    # Ensure publisher can only access their own data
    if publisher.id != publisher_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this publisher"
        )
    
    return publisher

@router.get("/{publisher_id}/integration-code", response_model=Dict[str, Any])
def generate_integration_code(
    publisher_id: str,
    publisher: PublisherModel = Depends(validate_api_key),
    db: Session = Depends(get_db)
):
    # Ensure publisher can only access their own integration code
    if publisher.id != publisher_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this publisher's integration code"
        )
    
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

@router.get("/{publisher_id}/tasks", response_model=TaskListResponse)
async def get_available_tasks(
    publisher_id: str,
    status: str = Query(None, enum=["PENDING", "AVAILABLE"]),
    limit: int = Query(10, ge=1, le=100),
    publisher: PublisherModel = Depends(validate_api_key),
    db: Session = Depends(get_db)
):
    # Ensure publisher can only access their tasks
    if publisher.id != publisher_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access these tasks"
        )
    
    # Get tasks from tasks service
    tasks = await publisher_crud.get_available_tasks(
        db=db,
        publisher_id=publisher_id,
        status=status,
        limit=limit
    )
    
    return TaskListResponse(total=len(tasks), items=tasks)

@router.patch("/{publisher_id}", response_model=Publisher)
def update_publisher_details(
    publisher_id: str,
    publisher_update: PublisherUpdate,
    publisher: PublisherModel = Depends(validate_api_key),
    db: Session = Depends(get_db)
):
    # Ensure publisher can only update their own data
    if publisher.id != publisher_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this publisher"
        )
    
    # Update publisher
    updated_publisher = publisher_crud.update_publisher(
        db=db,
        publisher_id=publisher_id,
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
    config_update: PublisherConfigurationUpdate,
    publisher: PublisherModel = Depends(validate_api_key),
    db: Session = Depends(get_db)
):
    # Ensure publisher can only update their own configuration
    if publisher.id != publisher_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this publisher's configuration"
        )
    
    # Update configuration
    updated_publisher = publisher_crud.update_publisher_configuration(
        db=db,
        publisher_id=publisher_id,
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
    start_date: datetime = Query(None),
    end_date: datetime = Query(None),
    publisher: PublisherModel = Depends(validate_api_key),
    db: Session = Depends(get_db)
):
    # Ensure publisher can only access their own statistics
    if publisher.id != publisher_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this publisher's statistics"
        )
    
    # Set default date range if not provided
    if not end_date:
        end_date = datetime.utcnow()
    if not start_date:
        start_date = end_date - timedelta(days=30)
    
    # Get statistics from tasks service
    return {
        "total_tasks": 100,  # Mock data for now
        "completed_tasks": 75,
        "pending_tasks": 25,
        "average_completion_time": "2h 30m",
        "quality_score": 4.5,
        "period": {
            "start": start_date.isoformat(),
            "end": end_date.isoformat()
        }
    }
