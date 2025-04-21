#!/bin/bash

# This script runs tests that match a specific keyword

# Check if keyword is provided
if [ -z "$1" ]; then
    echo "Error: No keyword provided."
    echo "Usage: $0 <keyword>"
    echo "Example: $0 publisher"
    exit 1
fi

KEYWORD=$1

# Run tests with the specified keyword
echo "Running tests matching keyword: $KEYWORD"
pytest -k "$KEYWORD" --cov=app --cov-report=term-missing

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "All tests matching keyword '$KEYWORD' passed!"
else
    echo "Some tests matching keyword '$KEYWORD' failed. Please check the output above for details."
fi
