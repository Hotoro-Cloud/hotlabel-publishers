#!/bin/bash

# This script runs tests and reports the slowest tests

# Check if number of tests to report is provided
if [ -z "$1" ]; then
    NUM_TESTS=10
else
    NUM_TESTS=$1
fi

echo "Running tests and reporting the $NUM_TESTS slowest tests..."
pytest --durations=$NUM_TESTS --cov=app --cov-report=term-missing

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "All tests passed!"
else
    echo "Some tests failed. Please check the output above for details."
fi
