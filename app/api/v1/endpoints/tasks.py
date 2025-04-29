from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from hotlabel_publishers.models import Publisher
from hotlabel_publishers.crud import publisher as crud
from hotlabel_publishers.database import get_db
from hotlabel_publishers.schemas.task import Task
from hotlabel_publishers.api.deps import get_current_publisher
from hotlabel_publishers.schemas.publisher import PublisherResponse

router = APIRouter()

@router.get("/{publisher_id}", response_model=PublisherResponse)
async def get_publisher(
    publisher_id: str,
    db: AsyncSession = Depends(get_db),
    current_publisher: Publisher = Depends(get_current_publisher)
):
    """Get publisher details."""
    if str(current_publisher.id) != publisher_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this publisher's details"
        )
    
    publisher = await crud.publisher.get_publisher(db, publisher_id)
    if not publisher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Publisher not found"
        )
    
    return publisher

@router.get("/available", response_model=List[Task])
async def get_available_tasks(
    publisher_id: str,
    db: AsyncSession = Depends(get_db),
    current_publisher: Publisher = Depends(get_current_publisher)
):
    """Get available tasks for a publisher."""
    if str(current_publisher.id) != publisher_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access tasks for this publisher"
        )
    
    tasks = await crud.publisher.get_available_tasks(publisher_id, db)
    return tasks 