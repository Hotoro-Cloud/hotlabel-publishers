import pytest
from fastapi import HTTPException
from unittest.mock import AsyncMock, MagicMock

from app.core.auth import validate_api_key
from app.models.publisher import Publisher

class TestAuth:
    async def test_validate_api_key_success(self, db_session):
        # Create a mock publisher in the database
        publisher = Publisher(
            id="pub_12345678",
            company_name="Test Publisher",
            website_url="https://example.com",
            contact_email="test@example.com",
            contact_name="Test User",
            website_categories=["news"],
            estimated_monthly_traffic=10000,
            integration_platform="custom",
            preferred_task_types=["survey"],
            api_key="test_api_key"
        )
        db_session.add(publisher)
        db_session.commit()
        
        # Test with valid API key
        api_key = "Bearer test_api_key"
        result = await validate_api_key(api_key, db_session)
        
        # Check that publisher was returned
        assert result is not None
        assert result.id == publisher.id
        assert result.api_key == "test_api_key"

    async def test_validate_api_key_missing(self, db_session):
        # Test with missing API key
        with pytest.raises(HTTPException) as excinfo:
            await validate_api_key(None, db_session)
        
        # Check that correct error was raised
        assert excinfo.value.status_code == 401
        assert excinfo.value.detail == "API key is missing"

    async def test_validate_api_key_invalid_format(self, db_session):
        # Test with invalid API key format (missing Bearer prefix)
        with pytest.raises(HTTPException) as excinfo:
            await validate_api_key("test_api_key", db_session)
        
        # Check that correct error was raised
        assert excinfo.value.status_code == 401
        assert excinfo.value.detail == "Invalid API key format"

    async def test_validate_api_key_invalid_key(self, db_session):
        # Test with invalid API key
        with pytest.raises(HTTPException) as excinfo:
            await validate_api_key("Bearer invalid_key", db_session)
        
        # Check that correct error was raised
        assert excinfo.value.status_code == 401
        assert excinfo.value.detail == "Invalid API key"
