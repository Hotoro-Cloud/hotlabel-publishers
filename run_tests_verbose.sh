#!/bin/bash

# This script runs tests with verbose output

echo "Running tests with verbose output..."
pytest -v --cov=app --cov-report=term-missing

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "All tests passed!"
else
    echo "Some tests failed. Please check the output above for details."
fi
