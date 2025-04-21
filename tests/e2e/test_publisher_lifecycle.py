import pytest
from fastapi.testclient import TestClient

class TestPublisherLifecycle:
    def test_complete_publisher_lifecycle(self, client: TestClient):
        """
        Test the complete lifecycle of a publisher:
        1. Register a new publisher
        2. Get publisher details
        3. Update publisher details
        4. Update publisher configuration
        5. Get publisher statistics
        6. Generate integration code
        7. Configure webhook
        8. Regenerate API key
        """
        # 1. Register a new publisher
        publisher_data = {
            "company_name": "Lifecycle Test Publisher",
            "website_url": "https://lifecycle-test.com",
            "contact_email": "lifecycle@example.com",
            "contact_name": "Lifecycle Test",
            "website_categories": ["news", "entertainment"],
            "estimated_monthly_traffic": 500000,
            "integration_platform": "wordpress",
            "preferred_task_types": ["survey", "feedback", "quiz"]
        }
        
        register_response = client.post("/api/v1/publishers", json=publisher_data)
        assert register_response.status_code == 201
        
        publisher = register_response.json()
        publisher_id = publisher["id"]
        api_key = publisher["api_key"]
        
        # 2. Get publisher details
        get_response = client.get(
            f"/api/v1/publishers/{publisher_id}",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        assert get_response.status_code == 200
        assert get_response.json()["id"] == publisher_id
        
        # 3. Update publisher details
        update_data = {
            "company_name": "Updated Lifecycle Publisher",
            "estimated_monthly_traffic": 750000
        }
        
        update_response = client.patch(
            f"/api/v1/publishers/{publisher_id}",
            json=update_data,
            headers={"Authorization": f"Bearer {api_key}"}
        )
        assert update_response.status_code == 200
        assert update_response.json()["company_name"] == "Updated Lifecycle Publisher"
        assert update_response.json()["estimated_monthly_traffic"] == 750000
        
        # 4. Update publisher configuration
        config_data = {
            "appearance": {
                "theme": "dark",
                "primary_color": "#FF5733",
                "border_radius": "8px"
            },
            "behavior": {
                "task_display_frequency": 180,
                "max_tasks_per_session": 10
            }
        }
        
        config_response = client.patch(
            f"/api/v1/publishers/{publisher_id}/configuration",
            json=config_data,
            headers={"Authorization": f"Bearer {api_key}"}
        )
        assert config_response.status_code == 200
        assert config_response.json()["success"] is True
        
        # 5. Get publisher statistics
        stats_response = client.get(
            f"/api/v1/publishers/{publisher_id}/statistics",
            params={"granularity": "daily"},
            headers={"Authorization": f"Bearer {api_key}"}
        )
        assert stats_response.status_code == 200
        assert "impression_metrics" in stats_response.json()
        assert "revenue_metrics" in stats_response.json()
        
        # 6. Generate integration code
        code_response = client.get(
            f"/api/v1/publishers/{publisher_id}/integration-code",
            params={"platform": "react"},
            headers={"Authorization": f"Bearer {api_key}"}
        )
        assert code_response.status_code == 200
        assert code_response.json()["platform"] == "react"
        assert "code_snippets" in code_response.json()
        
        # 7. Configure webhook
        webhook_data = {
            "endpoint_url": "https://lifecycle-test.com/webhook",
            "secret_key": "whsec_abcdefghijklmnop",
            "events": ["task.completed", "revenue.milestone.achieved"],
            "active": True
        }
        
        webhook_response = client.post(
            f"/api/v1/publishers/{publisher_id}/webhooks",
            json=webhook_data,
            headers={"Authorization": f"Bearer {api_key}"}
        )
        assert webhook_response.status_code == 200
        assert webhook_response.json()["status"] == "active"
        
        # 8. Regenerate API key
        regenerate_response = client.post(
            f"/api/v1/publishers/{publisher_id}/regenerate-api-key",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        assert regenerate_response.status_code == 200
        assert regenerate_response.json()["success"] is True
        
        new_api_key = regenerate_response.json()["api_key"]
        assert new_api_key != api_key
        
        # 9. Verify that old API key no longer works
        old_key_response = client.get(
            f"/api/v1/publishers/{publisher_id}",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        assert old_key_response.status_code == 401
        
        # 10. Verify that new API key works
        new_key_response = client.get(
            f"/api/v1/publishers/{publisher_id}",
            headers={"Authorization": f"Bearer {new_api_key}"}
        )
        assert new_key_response.status_code == 200
        assert new_key_response.json()["id"] == publisher_id
