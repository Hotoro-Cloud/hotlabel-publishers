#!/bin/bash

# This script runs tests and stops on the first failure

echo "Running tests and stopping on the first failure..."
pytest -xvs --cov=app --cov-report=term-missing

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "All tests passed!"
else
    echo "A test failed. Execution stopped at the first failure."
fi
