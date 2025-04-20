from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import secrets

from app.core.database import get_db
from app.core.auth import validate_api_key
from app.schemas.publisher import (
    Publisher, 
    PublisherCreate, 
    PublisherUpdate,
    PublisherConfigurationUpdate,
    PublisherStatisticsParams,
    IntegrationCodeParams,
    WebhookCreate
)
from app.crud import publisher as publisher_crud
from app.models.publisher import Publisher as PublisherModel

router = APIRouter(prefix="/publishers", tags=["publishers"])

@router.post("", response_model=Publisher, status_code=status.HTTP_201_CREATED)
def register_publisher(
    publisher_in: PublisherCreate,
    db: Session = Depends(get_db)
):
    # Check if publisher with this email already exists
    db_publisher = publisher_crud.get_publisher_by_email(db, email=publisher_in.contact_email)
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

@router.patch("/{publisher_id}/configuration", response_model=Dict[str, Any])
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
    
    return {
        "success": True,
        "updated_at": datetime.now(),
        "effective_from": datetime.now() + timedelta(minutes=5),
        "configuration_version": 1  # In a real implementation, this would be incremented
    }

@router.get("/{publisher_id}/statistics", response_model=Dict[str, Any])
def get_publisher_statistics(
    publisher_id: str,
    params: PublisherStatisticsParams = Depends(),
    publisher: PublisherModel = Depends(validate_api_key),
    db: Session = Depends(get_db)
):
    # Ensure publisher can only access their own statistics
    if publisher.id != publisher_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this publisher's statistics"
        )
    
    # Set default date range if not provided (last 7 days)
    end_date = params.end_date or datetime.now()
    start_date = params.start_date or (end_date - timedelta(days=7))
    
    # In a real implementation, this would query a statistics database or data warehouse
    # For now, return mock data
    return {
        "period": {
            "start": start_date,
            "end": end_date
        },
        "impression_metrics": {
            "total_impressions": 125400,
            "task_displays": 45200,
            "task_completions": 32150,
            "completion_rate": 0.71
        },
        "revenue_metrics": {
            "total_revenue": 642.75,
            "cpm": 5.12,
            "estimated_traditional_ad_revenue": 125.40,
            "revenue_uplift_percentage": 412.56
        },
        "user_metrics": {
            "unique_users": 28450,
            "returning_users": 12350,
            "average_tasks_per_user": 1.13
        },
        "time_series": [
            {
                "date": start_date + timedelta(days=i),
                "impressions": 17840 + i * 100,
                "completions": 4532 + i * 25,
                "revenue": 90.64 + i * 5.25
            } for i in range(7)
        ]
    }

@router.get("/{publisher_id}/integration-code", response_model=Dict[str, Any])
def generate_integration_code(
    publisher_id: str,
    params: IntegrationCodeParams = Depends(),
    publisher: PublisherModel = Depends(validate_api_key),
    db: Session = Depends(get_db)
):
    # Ensure publisher can only access their own integration code
    if publisher.id != publisher_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this publisher's integration code"
        )
    
    # Generate integration code based on platform
    platform = params.platform
    include_comments = params.include_comments
    
    # Basic integration code for all platforms
    header_code = f'<script src="https://cdn.hotlabel.io/sdk/v1/{publisher_id}.js"></script>'
    
    body_code = f'''<div id="hotlabel-container"></div>
<script>
HotLabel.init({{
  containerId: 'hotlabel-container',
  publisherId: '{publisher_id}',
  appearance: {{
    theme: '{publisher.configuration.get("appearance", {}).get("theme", "light")}',
    primaryColor: '{publisher.configuration.get("appearance", {}).get("primary_color", "#3366FF")}'
  }}
}});
</script>'''
    
    # Platform-specific installation steps
    installation_steps = []
    if platform == "wordpress":
        installation_steps = [
            "Install the HotLabel WordPress plugin from the WordPress plugin directory",
            f"Navigate to Settings > HotLabel in your WordPress admin",
            f"Enter your Publisher ID: {publisher_id}",
            "Save your settings and the integration is complete"
        ]
    elif platform == "react":
        installation_steps = [
            "Install the HotLabel React package: npm install hotlabel-react",
            f"Import and use the HotLabel component in your React application",
            f"Pass your Publisher ID as a prop: <HotLabel publisherId=\"{publisher_id}\" />"
        ]
    else:
        installation_steps = [
            "Add the HotLabel script to your website's header",
            "Add the container div and initialization code where you want the widget to appear"
        ]
    
    return {
        "platform": platform,
        "code_snippets": {
            "header": header_code,
            "body": body_code
        },
        "installation_steps": installation_steps,
        "documentation_url": f"https://docs.hotlabel.io/integration/{platform}"
    }

@router.post("/{publisher_id}/webhooks", response_model=Dict[str, Any])
def configure_webhook(
    publisher_id: str,
    webhook: WebhookCreate,
    publisher: PublisherModel = Depends(validate_api_key),
    db: Session = Depends(get_db)
):
    # Ensure publisher can only configure their own webhooks
    if publisher.id != publisher_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to configure webhooks for this publisher"
        )
    
    # In a real implementation, this would store the webhook configuration in the database
    # For now, return a mock response
    webhook_id = f"wh_{secrets.token_hex(5)}"
    
    return {
        "webhook_id": webhook_id,
        "status": "active" if webhook.active else "inactive",
        "test_event_url": f"https://api.hotlabel.io/v1/publishers/{publisher_id}/webhooks/{webhook_id}/test"
    }

@router.post("/{publisher_id}/regenerate-api-key", response_model=Dict[str, Any])
def regenerate_api_key(
    publisher_id: str,
    publisher: PublisherModel = Depends(validate_api_key),
    db: Session = Depends(get_db)
):
    # Ensure publisher can only regenerate their own API key
    if publisher.id != publisher_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to regenerate API key for this publisher"
        )
    
    new_api_key = publisher_crud.regenerate_api_key(db, publisher_id)
    if not new_api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Publisher not found"
        )
    
    return {
        "success": True,
        "api_key": new_api_key,
        "updated_at": datetime.now()
    }
