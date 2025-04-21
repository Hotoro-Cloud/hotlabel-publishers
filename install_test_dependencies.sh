#!/bin/bash

# This script installs all the required dependencies for testing

echo "Installing test dependencies..."
pip install -r requirements.txt

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo "All dependencies installed successfully!"
    echo "You can now run the tests using the provided scripts."
    echo "For example: ./run_tests.sh"
else
    echo "Failed to install dependencies. Please check the output above for details."
fi
