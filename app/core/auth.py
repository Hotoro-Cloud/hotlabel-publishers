from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from app.core.database import get_db

API_KEY_HEADER = APIKeyHeader(name="Authorization", auto_error=False)

async def validate_api_key(
    api_key: str = Depends(API_KEY_HEADER),
    db: Session = Depends(get_db)
):
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is missing",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    # Expected format: "Bearer <api_key>"
    if not api_key.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key format",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    # Extract the actual key
    key = api_key.replace("Bearer ", "")
    
    # Lazy import to avoid circular dependency
    from app.models.publisher import Publisher
    
    # Verify the key
    publisher = db.query(Publisher).filter(Publisher.api_key == key).first()
    if not publisher:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    return publisher
