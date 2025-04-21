#!/bin/bash

# This script runs tests in random order

echo "Running tests in random order..."
pytest --random-order --cov=app --cov-report=term-missing

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "All tests passed in random order!"
else
    echo "Some tests failed in random order. This might indicate test interdependencies."
    echo "Use the --random-order-seed from the output above to reproduce this specific test order."
fi
