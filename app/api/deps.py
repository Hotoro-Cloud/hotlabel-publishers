from typing import Optional
from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import publisher as crud
from app.models import Publisher

async def get_current_publisher(
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> Publisher:
    """Get the current publisher from the API key."""
    # Try to get API key from X-API-Key header first
    api_key = request.headers.get("X-API-Key")
    
    # If not found, try Authorization header
    if not api_key:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            api_key = auth_header.split(" ")[1]
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key not found in headers"
        )
    
    publisher = await crud.publisher.get_publisher_by_api_key(db, api_key)
    if not publisher:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    return publisher 