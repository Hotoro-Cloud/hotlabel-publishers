#!/bin/bash

# This script cleans up test artifacts

echo "Cleaning up test artifacts..."

# Remove coverage files
rm -rf .coverage
rm -rf htmlcov/
rm -rf coverage.xml

# Remove pytest cache
rm -rf .pytest_cache/

# Remove test reports
rm -rf test_reports/

# Remove __pycache__ directories
find . -type d -name "__pycache__" -exec rm -rf {} +

# Remove .pyc files
find . -name "*.pyc" -delete

echo "Test artifacts cleaned up successfully!"
