import pytest
from pydantic import AnyHttpUrl

from app.core.config import Settings

class TestSettings:
    def test_default_values(self):
        """Test that default values are set correctly."""
        settings = Settings()
        
        assert settings.API_V1_STR == "/api/v1"
        assert settings.PROJECT_NAME == "HotLabel Publisher Management"
        assert settings.POSTGRES_SERVER == "localhost"
        assert settings.POSTGRES_USER == "postgres"
        assert settings.POSTGRES_PASSWORD == "postgres"
        assert settings.POSTGRES_DB == "hotlabel_publishers"
        assert settings.REDIS_HOST == "localhost"
        assert settings.REDIS_PORT == 6379
        assert settings.REDIS_PASSWORD == ""
        assert isinstance(settings.CORS_ORIGINS, list)

    def test_sqlalchemy_database_uri_property(self):
        """Test that SQLALCHEMY_DATABASE_URI property works correctly."""
        # Test with default values
        settings = Settings()
        expected_uri = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}/{settings.POSTGRES_DB}"
        assert settings.SQLALCHEMY_DATABASE_URI == expected_uri
        
        # Test with custom DATABASE_URI
        custom_uri = "postgresql://user:pass@custom-server/custom-db"
        settings = Settings(DATABASE_URI=custom_uri)
        assert settings.SQLALCHEMY_DATABASE_URI == custom_uri

    def test_cors_origins_validation(self):
        """Test that CORS_ORIGINS are validated correctly."""
        # Valid URLs
        valid_urls = ["http://localhost", "https://example.com"]
        settings = Settings(CORS_ORIGINS=[AnyHttpUrl(url) for url in valid_urls])
        assert len(settings.CORS_ORIGINS) == 2
        assert str(settings.CORS_ORIGINS[0]) == "http://localhost"
        assert str(settings.CORS_ORIGINS[1]) == "https://example.com"
