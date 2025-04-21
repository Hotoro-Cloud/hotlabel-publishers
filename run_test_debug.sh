#!/bin/bash

# This script runs a specific test in debug mode

# Check if test ID is provided
if [ -z "$1" ]; then
    echo "Error: No test ID provided."
    echo "Usage: $0 <test_id>"
    echo "Example: $0 tests/unit/test_schemas.py::TestPublisherCreateSchema::test_valid_data"
    exit 1
fi

TEST_ID=$1

# Run the specified test in debug mode
echo "Running test with ID: $TEST_ID in debug mode..."
pytest "$TEST_ID" -v --no-header --showlocals --verbose

# Check if test passed
if [ $? -eq 0 ]; then
    echo "Test '$TEST_ID' passed!"
else
    echo "Test '$TEST_ID' failed. Please check the output above for details."
fi
