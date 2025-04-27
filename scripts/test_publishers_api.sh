#!/bin/bash

# Test script for publishers service API through Kong
# This script tests all endpoints of the publishers service

# Set variables
KONG_URL="http://localhost:8000"
PUBLISHERS_API_URL="${KONG_URL}/api/v1/publishers"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Function to print section headers
print_header() {
  echo -e "\n${YELLOW}=== $1 ===${NC}"
}

# Function to make API requests and check response
make_request() {
  local method=$1
  local url=$2
  local data=$3
  local expected_status=$4
  local api_key=$5
  
  echo -e "${YELLOW}Request:${NC} $method $url"
  if [ ! -z "$data" ]; then
    echo -e "${YELLOW}Data:${NC} $data"
  fi
  
  local headers=("-H" "Content-Type: application/json")
  if [ ! -z "$api_key" ]; then
    headers+=("-H" "Authorization: Bearer $api_key")
  fi
  
  if [ "$method" == "GET" ]; then
    response=$(curl -s -w "\n%{http_code}" -X $method "$url" "${headers[@]}")
  else
    response=$(curl -s -w "\n%{http_code}" -X $method "$url" "${headers[@]}" -d "$data")
  fi
  
  status_code=$(echo "$response" | tail -n1)
  response_body=$(echo "$response" | sed '$d')
  
  echo -e "${YELLOW}Status:${NC} $status_code"
  echo -e "${YELLOW}Response:${NC} $response_body"
  
  if [ "$status_code" == "$expected_status" ]; then
    echo -e "${GREEN}✓ Test passed${NC}"
    return 0
  else
    echo -e "${RED}✗ Test failed${NC}"
    return 1
  fi
}

# Test health endpoint
print_header "Testing Health Endpoint"
make_request "GET" "${PUBLISHERS_API_URL}/health" "" "200"

# Register a new publisher
print_header "Registering a new publisher"
timestamp=$(date +%s)
publisher_data='{
  "company_name": "Test Publisher",
  "website_url": "https://example.com",
  "contact_email": "test+'$timestamp'@example.com",
  "contact_name": "Test User",
  "website_categories": ["news", "technology"],
  "estimated_monthly_traffic": 100000,
  "integration_platform": "custom",
  "preferred_task_types": ["text_classification", "sentiment_analysis"]
}'
make_request "POST" "$PUBLISHERS_API_URL" "$publisher_data" "201"

# Extract publisher ID and API key from response
publisher_id=$(echo "$response_body" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
api_key=$(echo "$response_body" | grep -o '"api_key":"[^"]*"' | cut -d'"' -f4)

if [ -z "$publisher_id" ] || [ -z "$api_key" ]; then
  echo -e "${RED}Failed to extract publisher ID or API key from response${NC}"
  exit 1
fi

echo "Publisher ID: $publisher_id"
echo "API Key: $api_key"

# Get publisher details
print_header "Getting publisher details"
make_request "GET" "${PUBLISHERS_API_URL}/${publisher_id}" "" "200" "$api_key"

# Update publisher details
print_header "Updating publisher details"
update_data='{
  "company_name": "Updated Test Publisher",
  "website_url": "https://updated-example.com",
  "contact_name": "Updated Test User",
  "website_categories": ["news", "technology", "entertainment"],
  "estimated_monthly_traffic": 150000
}'
make_request "PATCH" "${PUBLISHERS_API_URL}/${publisher_id}" "$update_data" "200" "$api_key"

# Update publisher configuration
print_header "Updating publisher configuration"
config_data='{
  "appearance": {
    "theme": "dark",
    "primary_color": "#FF3366",
    "border_radius": "8px",
    "font_family": "Inter, sans-serif"
  },
  "behavior": {
    "task_display_frequency": 600,
    "max_tasks_per_session": 3,
    "show_task_after_seconds": 45,
    "display_on_page_types": ["article", "video", "gallery"]
  },
  "task_preferences": {
    "preferred_task_types": ["text_classification", "sentiment_analysis", "image_tagging"],
    "max_complexity_level": 2,
    "preferred_languages": ["en", "es"]
  },
  "rewards": {
    "content_access_duration_seconds": 7200,
    "show_completion_feedback": true
  }
}'
make_request "PATCH" "${PUBLISHERS_API_URL}/${publisher_id}/configuration" "$config_data" "200" "$api_key"

# Get publisher statistics
print_header "Getting publisher statistics"
make_request "GET" "${PUBLISHERS_API_URL}/${publisher_id}/statistics?granularity=daily" "" "200" "$api_key"

# Generate integration code
print_header "Generating integration code"
make_request "GET" "${PUBLISHERS_API_URL}/${publisher_id}/integration-code?platform=custom&include_comments=true" "" "200" "$api_key"

# Configure webhook
print_header "Configuring webhook"
webhook_data='{
  "endpoint_url": "https://example.com/webhook",
  "secret_key": "whsec_abcdef1234567890abcdef1234567890",
  "events": ["task.completed", "user.session.expired"],
  "active": true
}'
make_request "POST" "${PUBLISHERS_API_URL}/${publisher_id}/webhooks" "$webhook_data" "200" "$api_key"

# Regenerate API key
print_header "Regenerating API key"
make_request "POST" "${PUBLISHERS_API_URL}/${publisher_id}/regenerate-api-key" "" "200" "$api_key"

# Extract new API key
new_api_key=$(echo "$response_body" | grep -o '"api_key":"[^"]*"' | cut -d'"' -f4)
if [ -z "$new_api_key" ]; then
  echo -e "${RED}Failed to extract new API key from response${NC}"
  exit 1
fi

echo "New API Key: $new_api_key"

# Test API documentation endpoints
print_header "Testing API Documentation Endpoints"
make_request "GET" "${PUBLISHERS_API_URL}/docs" "" "200"
make_request "GET" "${PUBLISHERS_API_URL}/redoc" "" "200"
make_request "GET" "${PUBLISHERS_API_URL}/openapi.json" "" "200"

echo -e "\n${GREEN}All tests completed!${NC}" 