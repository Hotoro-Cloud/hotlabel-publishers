#!/bin/bash

# This script runs tests that match a specific path pattern

# Check if path pattern is provided
if [ -z "$1" ]; then
    echo "Error: No path pattern provided."
    echo "Usage: $0 <path_pattern>"
    echo "Example: $0 tests/unit/test_schemas.py"
    echo "Example: $0 tests/unit/test_*.py"
    exit 1
fi

PATH_PATTERN=$1

# Run tests with the specified path pattern
echo "Running tests matching path pattern: $PATH_PATTERN"
pytest "$PATH_PATTERN" --cov=app --cov-report=term-missing

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "All tests matching path pattern '$PATH_PATTERN' passed!"
else
    echo "Some tests matching path pattern '$PATH_PATTERN' failed. Please check the output above for details."
fi
