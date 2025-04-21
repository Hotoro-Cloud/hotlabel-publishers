import pytest
from fastapi.testclient import TestClient
from datetime import datetime

from app.main import app

class TestPublisherRoutes:
    def test_register_publisher(self, client: TestClient, sample_publisher_data):
        # Test publisher registration
        response = client.post("/api/v1/publishers", json=sample_publisher_data)
        
        # Check response
        assert response.status_code == 201
        data = response.json()
        assert data["company_name"] == sample_publisher_data["company_name"]
        assert data["contact_email"] == sample_publisher_data["contact_email"]
        assert "id" in data
        assert "api_key" in data
        assert data["is_active"] is True
        assert "created_at" in data
        assert "configuration" in data

    def test_register_publisher_duplicate_email(self, client: TestClient, sample_publisher_in_db):
        # Try to register publisher with duplicate email
        duplicate_data = {
            "company_name": "Duplicate Publisher",
            "website_url": "https://duplicate.com",
            "contact_email": sample_publisher_in_db.contact_email,  # Duplicate email
            "contact_name": "Duplicate User",
            "website_categories": ["news"],
            "estimated_monthly_traffic": 10000,
            "integration_platform": "custom",
            "preferred_task_types": ["survey"]
        }
        
        response = client.post("/api/v1/publishers", json=duplicate_data)
        
        # Check response
        assert response.status_code == 409
        assert response.json()["detail"] == "Publisher with this email already exists"

    def test_get_publisher(self, client: TestClient, sample_publisher_in_db):
        # Test get publisher endpoint
        response = client.get(
            f"/api/v1/publishers/{sample_publisher_in_db.id}",
            headers={"Authorization": f"Bearer {sample_publisher_in_db.api_key}"}
        )
        
        # Check response
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_publisher_in_db.id
        assert data["company_name"] == sample_publisher_in_db.company_name
        assert data["contact_email"] == sample_publisher_in_db.contact_email

    def test_get_publisher_unauthorized(self, client: TestClient, sample_publisher_in_db):
        # Test get publisher endpoint with invalid API key
        response = client.get(
            f"/api/v1/publishers/{sample_publisher_in_db.id}",
            headers={"Authorization": "Bearer invalid_key"}
        )
        
        # Check response
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid API key"

    def test_get_publisher_wrong_publisher(self, client: TestClient, sample_publisher_in_db):
        # Create another publisher
        other_publisher_data = {
            "company_name": "Other Publisher",
            "website_url": "https://other.com",
            "contact_email": "other@example.com",
            "contact_name": "Other User",
            "website_categories": ["news"],
            "estimated_monthly_traffic": 10000,
            "integration_platform": "custom",
            "preferred_task_types": ["survey"]
        }
        
        other_response = client.post("/api/v1/publishers", json=other_publisher_data)
        other_publisher_id = other_response.json()["id"]
        
        # Try to get other publisher with sample publisher's API key
        response = client.get(
            f"/api/v1/publishers/{other_publisher_id}",
            headers={"Authorization": f"Bearer {sample_publisher_in_db.api_key}"}
        )
        
        # Check response
        assert response.status_code == 403
        assert response.json()["detail"] == "Not authorized to access this publisher"

    def test_update_publisher(self, client: TestClient, sample_publisher_in_db):
        # Test update publisher endpoint
        update_data = {
            "company_name": "Updated Publisher",
            "contact_email": "updated@example.com"
        }
        
        response = client.patch(
            f"/api/v1/publishers/{sample_publisher_in_db.id}",
            json=update_data,
            headers={"Authorization": f"Bearer {sample_publisher_in_db.api_key}"}
        )
        
        # Check response
        assert response.status_code == 200
        data = response.json()
        assert data["company_name"] == "Updated Publisher"
        assert data["contact_email"] == "updated@example.com"
        assert data["id"] == sample_publisher_in_db.id

    def test_update_publisher_unauthorized(self, client: TestClient, sample_publisher_in_db):
        # Test update publisher endpoint with invalid API key
        update_data = {"company_name": "Updated Publisher"}
        
        response = client.patch(
            f"/api/v1/publishers/{sample_publisher_in_db.id}",
            json=update_data,
            headers={"Authorization": "Bearer invalid_key"}
        )
        
        # Check response
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid API key"

    def test_update_publisher_configuration(self, client: TestClient, sample_publisher_in_db):
        # Test update publisher configuration endpoint
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
        
        response = client.patch(
            f"/api/v1/publishers/{sample_publisher_in_db.id}/configuration",
            json=config_data,
            headers={"Authorization": f"Bearer {sample_publisher_in_db.api_key}"}
        )
        
        # Check response
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "updated_at" in data
        assert "effective_from" in data
        assert "configuration_version" in data

    def test_get_publisher_statistics(self, client: TestClient, sample_publisher_in_db):
        # Test get publisher statistics endpoint
        response = client.get(
            f"/api/v1/publishers/{sample_publisher_in_db.id}/statistics",
            headers={"Authorization": f"Bearer {sample_publisher_in_db.api_key}"}
        )
        
        # Check response
        assert response.status_code == 200
        data = response.json()
        assert "period" in data
        assert "impression_metrics" in data
        assert "revenue_metrics" in data
        assert "user_metrics" in data
        assert "time_series" in data

    def test_get_publisher_statistics_with_params(self, client: TestClient, sample_publisher_in_db):
        # Test get publisher statistics endpoint with parameters
        start_date = "2023-01-01T00:00:00"
        end_date = "2023-01-31T23:59:59"
        
        response = client.get(
            f"/api/v1/publishers/{sample_publisher_in_db.id}/statistics",
            params={"start_date": start_date, "end_date": end_date, "granularity": "weekly"},
            headers={"Authorization": f"Bearer {sample_publisher_in_db.api_key}"}
        )
        
        # Check response
        assert response.status_code == 200
        data = response.json()
        assert "period" in data
        assert data["period"]["start"].startswith("2023-01-01")
        assert data["period"]["end"].startswith("2023-01-31")

    def test_generate_integration_code(self, client: TestClient, sample_publisher_in_db):
        # Test generate integration code endpoint
        response = client.get(
            f"/api/v1/publishers/{sample_publisher_in_db.id}/integration-code",
            params={"platform": "wordpress", "include_comments": "true"},
            headers={"Authorization": f"Bearer {sample_publisher_in_db.api_key}"}
        )
        
        # Check response
        assert response.status_code == 200
        data = response.json()
        assert data["platform"] == "wordpress"
        assert "code_snippets" in data
        assert "header" in data["code_snippets"]
        assert "body" in data["code_snippets"]
        assert "installation_steps" in data
        assert "documentation_url" in data

    def test_configure_webhook(self, client: TestClient, sample_publisher_in_db):
        # Test configure webhook endpoint
        webhook_data = {
            "endpoint_url": "https://example.com/webhook",
            "secret_key": "whsec_abcdefghijklmnop",
            "events": ["task.completed", "user.session.expired"],
            "active": True
        }
        
        response = client.post(
            f"/api/v1/publishers/{sample_publisher_in_db.id}/webhooks",
            json=webhook_data,
            headers={"Authorization": f"Bearer {sample_publisher_in_db.api_key}"}
        )
        
        # Check response
        assert response.status_code == 200
        data = response.json()
        assert "webhook_id" in data
        assert data["status"] == "active"
        assert "test_event_url" in data

    def test_regenerate_api_key(self, client: TestClient, sample_publisher_in_db):
        # Store original API key
        original_api_key = sample_publisher_in_db.api_key
        
        # Test regenerate API key endpoint
        response = client.post(
            f"/api/v1/publishers/{sample_publisher_in_db.id}/regenerate-api-key",
            headers={"Authorization": f"Bearer {original_api_key}"}
        )
        
        # Check response
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "api_key" in data
        assert data["api_key"] != original_api_key
        assert "updated_at" in data
