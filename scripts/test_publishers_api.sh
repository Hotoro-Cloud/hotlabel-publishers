#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Kong API Gateway URL
KONG_URL="http://localhost:8000"

# Temporary file for response
TEMP_RESPONSE="/tmp/publisher_response.json"

# Generate unique timestamp for email
TIMESTAMP=$(date +%s)

# Function to print section headers
print_header() {
    echo -e "\n${GREEN}=== $1 ===${NC}"
}

# Function to make API requests
make_request() {
    local method=$1
    local endpoint=$2
    local data=$3
    local headers=$4
    
    echo "Making $method request to $endpoint"
    if [ -n "$data" ]; then
        if [ -n "$headers" ]; then
            curl -s -X $method "$KONG_URL$endpoint" \
                -H "Content-Type: application/json" \
                -H "$headers" \
                -d "$data" > "$TEMP_RESPONSE"
        else
            curl -s -X $method "$KONG_URL$endpoint" \
                -H "Content-Type: application/json" \
                -d "$data" > "$TEMP_RESPONSE"
        fi
    else
        if [ -n "$headers" ]; then
            curl -s -X $method "$KONG_URL$endpoint" \
                -H "$headers" > "$TEMP_RESPONSE"
        else
            curl -s -X $method "$KONG_URL$endpoint" > "$TEMP_RESPONSE"
        fi
    fi
    
    # Display formatted response
    if [ -s "$TEMP_RESPONSE" ]; then
        jq . "$TEMP_RESPONSE" || cat "$TEMP_RESPONSE"
    fi
    echo
}

# Test health check
print_header "Testing Health Check"
make_request "GET" "/api/v1/publishers/health"

# Test publisher registration
print_header "Testing Publisher Registration"
REGISTER_DATA='{
    "name": "Test Company",
    "website": "https://testcompany.com",
    "email": "test+'$TIMESTAMP'@testcompany.com",
    "description": "A test company for API testing"
}'

# Register publisher and capture response
make_request "POST" "/api/v1/publishers" "$REGISTER_DATA"

# Extract publisher ID and API key from response file
if [ -s "$TEMP_RESPONSE" ]; then
    PUBLISHER_ID=$(jq -r '.id // empty' "$TEMP_RESPONSE")
    API_KEY=$(jq -r '.api_key // empty' "$TEMP_RESPONSE")
    
    if [ -z "$PUBLISHER_ID" ] || [ -z "$API_KEY" ]; then
        echo "Error: Failed to extract publisher ID or API key from response"
        cat "$TEMP_RESPONSE"
        exit 1
    fi
    
    echo "Publisher ID: $PUBLISHER_ID"
    echo "API Key: $API_KEY"
else
    echo "Error: No response received from registration"
    exit 1
fi

# Test publisher details update
print_header "Testing Publisher Update"
UPDATE_DATA='{
    "name": "Updated Company",
    "description": "Updated description for testing"
}'
make_request "PATCH" "/api/v1/publishers/$PUBLISHER_ID" "$UPDATE_DATA" "Authorization: Bearer $API_KEY"

# Test publisher configuration
print_header "Testing Publisher Configuration"
CONFIG_DATA='{
    "appearance": {
        "theme": "light",
        "primary_color": "#007bff"
    },
    "behavior": {
        "auto_assign": true,
        "max_tasks_per_user": 10
    }
}'
make_request "PATCH" "/api/v1/publishers/$PUBLISHER_ID/configuration" "$CONFIG_DATA" "Authorization: Bearer $API_KEY"

# Test getting publisher statistics
print_header "Testing Publisher Statistics"
make_request "GET" "/api/v1/publishers/$PUBLISHER_ID/statistics" "" "Authorization: Bearer $API_KEY"

# Cleanup
rm -f "$TEMP_RESPONSE"

echo -e "\n${GREEN}Test script completed${NC}" 