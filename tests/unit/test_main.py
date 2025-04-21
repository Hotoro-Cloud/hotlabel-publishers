import pytest
from fastapi.testclient import TestClient

from app.main import app

class TestMainApp:
    def test_health_check(self, client: TestClient):
        """Test the health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code == 200
        assert response.json() == {
            "status": "healthy", 
            "service": "publisher-management"
        }

    def test_root_redirect(self, client: TestClient):
        """Test the root endpoint redirects to docs."""
        response = client.get("/")
        
        assert response.status_code == 200
        assert "message" in response.json()
        assert "docs" in response.json()
        assert response.json()["message"] == "HotLabel Publisher Management Service API"

    def test_docs_endpoint(self, client: TestClient):
        """Test the docs endpoint."""
        response = client.get("/api/v1/docs")
        
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_redoc_endpoint(self, client: TestClient):
        """Test the redoc endpoint."""
        response = client.get("/api/v1/redoc")
        
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_openapi_endpoint(self, client: TestClient):
        """Test the openapi endpoint."""
        response = client.get("/api/v1/openapi.json")
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        assert "openapi" in response.json()
        assert "info" in response.json()
        assert "paths" in response.json()
