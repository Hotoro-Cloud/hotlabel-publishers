#!/bin/bash

# This script runs tests with a specific marker

# Check if marker is provided
if [ -z "$1" ]; then
    echo "Error: No marker provided."
    echo "Usage: $0 <marker>"
    echo "Available markers: unit, integration, e2e, schemas, crud, auth, api, db"
    exit 1
fi

MARKER=$1

# Run tests with the specified marker
echo "Running tests with marker: $MARKER"
pytest -m "$MARKER" --cov=app --cov-report=term-missing

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "All tests with marker '$MARKER' passed!"
else
    echo "Some tests with marker '$MARKER' failed. Please check the output above for details."
fi
