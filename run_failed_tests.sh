#!/bin/bash

# This script runs only the tests that failed in the previous run

echo "Running only the tests that failed in the previous run..."
pytest --lf --cov=app --cov-report=term-missing

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "All previously failed tests now pass!"
else
    echo "Some tests are still failing. Please check the output above for details."
fi
