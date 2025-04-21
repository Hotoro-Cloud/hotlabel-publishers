import pytest
from pydantic import ValidationError
from datetime import datetime

from app.schemas.publisher import (
    PublisherCreate,
    PublisherUpdate,
    PublisherConfigurationUpdate,
    PublisherStatisticsParams,
    IntegrationCodeParams,
    WebhookCreate
)

class TestPublisherCreateSchema:
    def test_valid_data(self, sample_publisher_data):
        # Test with valid data
        publisher = PublisherCreate(**sample_publisher_data)
        assert publisher.company_name == sample_publisher_data["company_name"]
        assert str(publisher.website_url) == sample_publisher_data["website_url"]
        assert publisher.contact_email == sample_publisher_data["contact_email"]
        assert publisher.contact_name == sample_publisher_data["contact_name"]
        assert publisher.website_categories == sample_publisher_data["website_categories"]
        assert publisher.estimated_monthly_traffic == sample_publisher_data["estimated_monthly_traffic"]
        assert publisher.integration_platform == sample_publisher_data["integration_platform"]
        assert publisher.preferred_task_types == sample_publisher_data["preferred_task_types"]

    def test_invalid_email(self, sample_publisher_data):
        # Test with invalid email
        invalid_data = sample_publisher_data.copy()
        invalid_data["contact_email"] = "invalid-email"
        
        with pytest.raises(ValidationError):
            PublisherCreate(**invalid_data)

    def test_invalid_url(self, sample_publisher_data):
        # Test with invalid URL
        invalid_data = sample_publisher_data.copy()
        invalid_data["website_url"] = "invalid-url"
        
        with pytest.raises(ValidationError):
            PublisherCreate(**invalid_data)

    def test_missing_required_field(self, sample_publisher_data):
        # Test with missing required field
        invalid_data = sample_publisher_data.copy()
        del invalid_data["company_name"]
        
        with pytest.raises(ValidationError):
            PublisherCreate(**invalid_data)

class TestPublisherUpdateSchema:
    def test_valid_partial_update(self):
        # Test with valid partial update
        update_data = {
            "company_name": "Updated Publisher",
            "contact_email": "updated@example.com"
        }
        
        publisher_update = PublisherUpdate(**update_data)
        assert publisher_update.company_name == "Updated Publisher"
        assert publisher_update.contact_email == "updated@example.com"
        assert publisher_update.website_url is None
        assert publisher_update.contact_name is None
        assert publisher_update.website_categories is None
        assert publisher_update.estimated_monthly_traffic is None
        assert publisher_update.integration_platform is None
        assert publisher_update.preferred_task_types is None
        assert publisher_update.is_active is None

    def test_invalid_email_in_update(self):
        # Test with invalid email in update
        update_data = {
            "contact_email": "invalid-email"
        }
        
        with pytest.raises(ValidationError):
            PublisherUpdate(**update_data)

class TestPublisherConfigurationUpdateSchema:
    def test_valid_configuration_update(self):
        # Test with valid configuration update
        config_data = {
            "appearance": {
                "theme": "dark",
                "primary_color": "#FF5733"
            },
            "behavior": {
                "task_display_frequency": 600,
                "max_tasks_per_session": 3
            }
        }
        
        config_update = PublisherConfigurationUpdate(**config_data)
        assert config_update.appearance == config_data["appearance"]
        assert config_update.behavior == config_data["behavior"]
        assert config_update.task_preferences is None
        assert config_update.rewards is None

    def test_empty_configuration_update(self):
        # Test with empty configuration update
        config_update = PublisherConfigurationUpdate()
        assert config_update.appearance is None
        assert config_update.behavior is None
        assert config_update.task_preferences is None
        assert config_update.rewards is None

class TestPublisherStatisticsParamsSchema:
    def test_valid_statistics_params(self):
        # Test with valid statistics parameters
        now = datetime.now()
        params_data = {
            "start_date": now,
            "end_date": now,
            "granularity": "daily"
        }
        
        params = PublisherStatisticsParams(**params_data)
        assert params.start_date == now
        assert params.end_date == now
        assert params.granularity == "daily"

    def test_default_values(self):
        # Test default values
        params = PublisherStatisticsParams()
        assert params.start_date is None
        assert params.end_date is None
        assert params.granularity == "daily"

    def test_invalid_granularity(self):
        # Test with invalid granularity
        params_data = {
            "granularity": "invalid"
        }
        
        with pytest.raises(ValidationError):
            PublisherStatisticsParams(**params_data)

class TestIntegrationCodeParamsSchema:
    def test_valid_integration_code_params(self):
        # Test with valid integration code parameters
        params_data = {
            "platform": "wordpress",
            "include_comments": True
        }
        
        params = IntegrationCodeParams(**params_data)
        assert params.platform == "wordpress"
        assert params.include_comments is True

    def test_default_values(self):
        # Test default values
        params = IntegrationCodeParams()
        assert params.platform == "custom"
        assert params.include_comments is True

    def test_invalid_platform(self):
        # Test with invalid platform
        params_data = {
            "platform": "invalid"
        }
        
        with pytest.raises(ValidationError):
            IntegrationCodeParams(**params_data)

class TestWebhookCreateSchema:
    def test_valid_webhook_create(self):
        # Test with valid webhook create data
        webhook_data = {
            "endpoint_url": "https://example.com/webhook",
            "secret_key": "whsec_abcdefghijklmnop",
            "events": ["task.completed", "user.session.expired"],
            "active": True
        }
        
        webhook = WebhookCreate(**webhook_data)
        assert str(webhook.endpoint_url) == webhook_data["endpoint_url"]
        assert webhook.secret_key == webhook_data["secret_key"]
        assert webhook.events == webhook_data["events"]
        assert webhook.active is True

    def test_invalid_secret_key_format(self):
        # Test with invalid secret key format
        webhook_data = {
            "endpoint_url": "https://example.com/webhook",
            "secret_key": "invalid-secret",
            "events": ["task.completed"]
        }
        
        with pytest.raises(ValidationError):
            WebhookCreate(**webhook_data)

    def test_invalid_event(self):
        # Test with invalid event
        webhook_data = {
            "endpoint_url": "https://example.com/webhook",
            "secret_key": "whsec_abcdefghijklmnop",
            "events": ["invalid.event"]
        }
        
        with pytest.raises(ValidationError):
            WebhookCreate(**webhook_data)
