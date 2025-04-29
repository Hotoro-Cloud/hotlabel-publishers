from fastapi import Depends, HTTPException, status, Request
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
import logging
import asyncio

from app.core.database import get_db
from app.core.config import settings

logger = logging.getLogger(__name__)

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=True)

def is_internal_service(request: Request) -> bool:
    """Check if the request is coming from an internal service."""
    client_host = request.client.host if request.client else None
    logger.debug(f"Checking if request from {client_host} is an internal service")
    
    # Check if request is coming from Kong (internal network)
    is_internal = client_host in ["tasks", "localhost", "172.19.0.3"]
    
    # Also check for X-Internal-Service header that Kong can set
    internal_header = request.headers.get("X-Internal-Service")
    if internal_header:
        logger.debug(f"Found X-Internal-Service header: {internal_header}")
        is_internal = True
    
    logger.info(f"Request from {client_host} is{' ' if is_internal else ' not '}an internal service")
    return is_internal

def validate_api_key(
    request: Request,
    api_key: str = Depends(API_KEY_HEADER),
    db: Session = Depends(get_db)
):
    """Validate API key and return the associated publisher."""
    logger.info("Starting API key validation")
    logger.debug(f"Request headers: {dict(request.headers)}")
    
    try:
        # Allow internal service calls without API key
        if is_internal_service(request):
            logger.info("Internal service request detected")
            # For internal calls, we still need a publisher ID
            publisher_id = request.path_params.get("publisher_id")
            logger.debug(f"Publisher ID from path params: {publisher_id}")
            
            if publisher_id:
                # Lazy import to avoid circular dependency
                from app.models.publisher import Publisher
                logger.info(f"Looking up publisher with ID: {publisher_id}")
                publisher = db.query(Publisher).filter(Publisher.id == publisher_id).first()
                if publisher:
                    logger.info(f"Found publisher {publisher_id} for internal service request")
                    return publisher
                else:
                    logger.error(f"Publisher {publisher_id} not found for internal service request")
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Publisher not found"
                    )
        
        # Lazy import to avoid circular dependency
        from app.models.publisher import Publisher
        
        # Verify the key
        logger.info("Looking up publisher by API key")
        publisher = db.query(Publisher).filter(Publisher.api_key == api_key).first()
        if not publisher:
            logger.warning("No publisher found with provided API key")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key",
                headers={"WWW-Authenticate": "ApiKey"},
            )
        
        if not publisher.is_active:
            logger.warning(f"Publisher {publisher.id} is not active")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Publisher account is not active"
            )
        
        logger.info(f"Successfully validated API key for publisher {publisher.id}")
        return publisher
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error in validate_api_key: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"API key validation error: {str(e)}"
        )
