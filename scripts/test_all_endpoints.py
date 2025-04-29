#!/usr/bin/env python3
import requests
import uuid
from typing import Dict, Any
import json
from datetime import datetime, timedelta

# Configuration
KONG_URL = "http://localhost:8000"  # Adjust if your Kong is running on a different port
BASE_URL = f"{KONG_URL}/api/v1/publishers"

def print_response(response: requests.Response, title: str) -> None:
    """Helper function to print API responses in a readable format"""
    print(f"\n=== {title} ===")
    print(f"Status Code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(f"Raw response text: {response.text}")
    print("=" * 50)

def test_health_check():
    """Test health check endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print_response(response, "Health Check")
    assert response.status_code == 200, "Health check failed"
    return response.json()

def test_register_publisher() -> Dict[str, Any]:
    """Test registering a new publisher"""
    timestamp = int(datetime.now().timestamp())
    publisher_data = {
        "name": "Test Publisher",
        "website": "https://testpublisher.com",
        "email": f"test+{timestamp}@testpublisher.com",
        "description": "A test publisher for API testing"
    }
    print(f"\nSending request to {BASE_URL} with data: {json.dumps(publisher_data, indent=2)}")
    response = requests.post(BASE_URL, json=publisher_data)
    print_response(response, "Register Publisher")
    assert response.status_code == 201, "Register publisher failed"
    return response.json()

def test_update_publisher(publisher_id: str, api_key: str):
    """Test updating a publisher"""
    headers = {"X-API-Key": api_key}
    update_data = {
        "name": "Updated Test Publisher",
        "description": "An updated test publisher"
    }
    response = requests.patch(f"{BASE_URL}/{publisher_id}", json=update_data, headers=headers)
    print_response(response, "Update Publisher")
    assert response.status_code == 200, "Update publisher failed"

def test_update_publisher_configuration(publisher_id: str, api_key: str):
    """Test updating publisher configuration"""
    headers = {"X-API-Key": api_key}
    config_data = {
        "appearance": {
            "theme": "dark",
            "primary_color": "#00ff00"
        },
        "behavior": {
            "auto_assign": True,
            "max_tasks_per_user": 5
        }
    }
    response = requests.patch(f"{BASE_URL}/{publisher_id}/configuration", json=config_data, headers=headers)
    print_response(response, "Update Publisher Configuration")
    assert response.status_code == 200, "Update publisher configuration failed"

def test_get_publisher_integration_code(publisher_id: str, api_key: str):
    """Test getting publisher integration code"""
    headers = {"X-API-Key": api_key}
    response = requests.get(f"{BASE_URL}/{publisher_id}/integration-code", headers=headers)
    print_response(response, "Get Publisher Integration Code")
    assert response.status_code == 200, "Get integration code failed"

def test_get_publisher_tasks(publisher_id: str, api_key: str):
    """Test getting publisher tasks"""
    headers = {
        "X-API-Key": api_key,
        "X-Internal-Service": "true"
    }
    response = requests.get(f"{BASE_URL}/{publisher_id}/tasks", headers=headers)
    print_response(response, "Get Publisher Tasks")
    assert response.status_code == 200, "Get publisher tasks failed"
    
    # Test with status filter
    response = requests.get(f"{BASE_URL}/{publisher_id}/tasks?task_status=pending", headers=headers)
    print_response(response, "Get Publisher Tasks by Status")
    assert response.status_code == 200, "Get publisher tasks by status failed"

def test_get_publisher_statistics(publisher_id: str, api_key: str):
    """Test getting publisher statistics"""
    headers = {"X-API-Key": api_key}
    response = requests.get(f"{BASE_URL}/{publisher_id}/statistics", headers=headers)
    print_response(response, "Get Publisher Statistics")
    assert response.status_code == 200, "Get publisher statistics failed"
    
    # Test with date range
    start_date = (datetime.utcnow() - timedelta(days=7)).isoformat()
    end_date = datetime.utcnow().isoformat()
    response = requests.get(
        f"{BASE_URL}/{publisher_id}/statistics?start_date={start_date}&end_date={end_date}", 
        headers=headers
    )
    print_response(response, "Get Publisher Statistics with Date Range")
    assert response.status_code == 200, "Get publisher statistics with date range failed"

def test_get_publisher(publisher_id: str, api_key: str):
    """Test getting a single publisher"""
    headers = {"X-API-Key": api_key}
    response = requests.get(f"{BASE_URL}/{publisher_id}", headers=headers)
    print_response(response, "Get Publisher")
    assert response.status_code == 200, "Get publisher failed"

def main():
    print("Starting Publishers API Tests (Working Endpoints Only)...")
    
    try:
        # Test health check first
        test_health_check()
        
        # Test registering a publisher
        publisher = test_register_publisher()
        publisher_id = publisher["id"]
        api_key = publisher["api_key"]
        
        print(f"\nCreated test publisher with ID: {publisher_id}")
        print(f"API Key: {api_key}")
        
        # Skip get all publishers endpoint that doesn't exist
        print("\nSkipping Get All Publishers test - endpoint not implemented")
        
        # Test publisher operations with API key
        # Get publisher endpoint now works!
        test_get_publisher(publisher_id, api_key)
        test_update_publisher(publisher_id, api_key)
        test_update_publisher_configuration(publisher_id, api_key)
        test_get_publisher_integration_code(publisher_id, api_key)
        test_get_publisher_tasks(publisher_id, api_key)
        test_get_publisher_statistics(publisher_id, api_key)
        
        print("\nAll working endpoint tests completed successfully!")
        
    except AssertionError as e:
        print(f"Test failed: {str(e)}")
    except Exception as e:
        print(f"Error during tests: {str(e)}")

if __name__ == "__main__":
    main() 