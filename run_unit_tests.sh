#!/bin/bash

# Run unit tests with coverage
echo "Running unit tests with coverage..."
pytest tests/unit/ --cov=app --cov-report=term-missing

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "All unit tests passed!"
else
    echo "Some unit tests failed. Please check the output above for details."
fi
