import pytest
from datetime import datetime
import uuid
import secrets

from app.models.publisher import Publisher

class TestPublisherModel:
    def test_publisher_model_creation(self):
        """Test that a Publisher model can be created with required fields."""
        publisher = Publisher(
            company_name="Test Company",
            website_url="https://example.com",
            contact_email="test@example.com",
            contact_name="Test User",
            website_categories=["news"],
            estimated_monthly_traffic=10000,
            integration_platform="custom",
            preferred_task_types=["survey"]
        )
        
        assert publisher.company_name == "Test Company"
        assert publisher.website_url == "https://example.com"
        assert publisher.contact_email == "test@example.com"
        assert publisher.contact_name == "Test User"
        assert publisher.website_categories == ["news"]
        assert publisher.estimated_monthly_traffic == 10000
        assert publisher.integration_platform == "custom"
        assert publisher.preferred_task_types == ["survey"]
        
        # Default values
        assert publisher.is_active is True
        assert publisher.configuration == {}
        assert publisher.id is not None
        assert publisher.id.startswith("pub_")
        assert publisher.api_key is not None
        assert publisher.api_key.startswith("pk_live_")

    def test_publisher_model_with_custom_id_and_api_key(self):
        """Test that a Publisher model can be created with custom ID and API key."""
        custom_id = "pub_custom123"
        custom_api_key = "pk_live_custom123"
        
        publisher = Publisher(
            id=custom_id,
            api_key=custom_api_key,
            company_name="Custom ID Company",
            website_url="https://custom-id.com",
            contact_email="custom@example.com",
            contact_name="Custom User",
            website_categories=["news"],
            estimated_monthly_traffic=10000,
            integration_platform="custom",
            preferred_task_types=["survey"]
        )
        
        assert publisher.id == custom_id
        assert publisher.api_key == custom_api_key

    def test_publisher_model_with_configuration(self):
        """Test that a Publisher model can be created with configuration."""
        config = {
            "appearance": {
                "theme": "dark",
                "primary_color": "#FF5733"
            },
            "behavior": {
                "task_display_frequency": 600,
                "max_tasks_per_session": 3
            }
        }
        
        publisher = Publisher(
            company_name="Config Company",
            website_url="https://config.com",
            contact_email="config@example.com",
            contact_name="Config User",
            website_categories=["news"],
            estimated_monthly_traffic=10000,
            integration_platform="custom",
            preferred_task_types=["survey"],
            configuration=config
        )
        
        assert publisher.configuration == config
        assert publisher.configuration["appearance"]["theme"] == "dark"
        assert publisher.configuration["behavior"]["task_display_frequency"] == 600

    def test_publisher_model_timestamps(self, db_session):
        """Test that timestamps are set correctly when a publisher is created."""
        publisher = Publisher(
            company_name="Timestamp Company",
            website_url="https://timestamp.com",
            contact_email="timestamp@example.com",
            contact_name="Timestamp User",
            website_categories=["news"],
            estimated_monthly_traffic=10000,
            integration_platform="custom",
            preferred_task_types=["survey"]
        )
        
        # Add to session and commit to trigger timestamp creation
        db_session.add(publisher)
        db_session.commit()
        
        assert publisher.created_at is not None
        assert isinstance(publisher.created_at, datetime)
        
        # updated_at should be None initially
        assert publisher.updated_at is None
        
        # Update the publisher to trigger updated_at
        publisher.company_name = "Updated Timestamp Company"
        db_session.commit()
        
        assert publisher.updated_at is not None
        assert isinstance(publisher.updated_at, datetime)
        assert publisher.updated_at > publisher.created_at
