#!/bin/bash

# This script runs the tests in a Docker container to ensure a clean environment

# Build a test image based on the Dockerfile
echo "Building test Docker image..."
docker build -t hotlabel-publishers-test .

# Run the tests in the container
echo "Running tests in Docker container..."
docker run --rm \
  -v "$(pwd):/app" \
  -w /app \
  hotlabel-publishers-test \
  pytest --cov=app --cov-report=term-missing --cov-report=html

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "All tests passed in Docker container!"
    echo "Coverage report generated in htmlcov/ directory"
    echo "Open htmlcov/index.html in your browser to view the report"
else
    echo "Some tests failed in Docker container. Please check the output above for details."
fi
