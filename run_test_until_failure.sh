#!/bin/bash

# This script runs a specific test repeatedly until it fails

# Check if test ID is provided
if [ -z "$1" ]; then
    echo "Error: No test ID provided."
    echo "Usage: $0 <test_id> [max_iterations]"
    echo "Example: $0 tests/unit/test_schemas.py::TestPublisherCreateSchema::test_valid_data 100"
    exit 1
fi

TEST_ID=$1

# Check if max iterations is provided
if [ -z "$2" ]; then
    MAX_ITERATIONS=100
else
    MAX_ITERATIONS=$2
fi

echo "Running test with ID: $TEST_ID repeatedly until failure (max $MAX_ITERATIONS iterations)..."

# Initialize counter
COUNTER=1

# Run test repeatedly until failure or max iterations
while [ $COUNTER -le $MAX_ITERATIONS ]
do
    echo "Iteration $COUNTER of $MAX_ITERATIONS"
    pytest "$TEST_ID" -v
    
    # Check if test failed
    if [ $? -ne 0 ]; then
        echo "Test failed on iteration $COUNTER"
        exit 1
    fi
    
    # Increment counter
    COUNTER=$((COUNTER+1))
done

echo "Test passed all $MAX_ITERATIONS iterations"
