#!/bin/bash

# This script runs tests in parallel using pytest-xdist

# Check if number of processes is provided
if [ -z "$1" ]; then
    # Default to number of CPU cores
    NUM_PROCESSES=$(nproc)
else
    NUM_PROCESSES=$1
fi

echo "Running tests in parallel with $NUM_PROCESSES processes..."
pytest -xvs -n $NUM_PROCESSES --cov=app --cov-report=term-missing

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "All tests passed!"
else
    echo "Some tests failed. Please check the output above for details."
fi
