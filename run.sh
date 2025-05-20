#!/bin/bash
set -e

echo "Preparing environment..."

# Set environment variables
export $(grep -v '^#' .env | xargs -d '\n')

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies and Playwright browsers
pip install -r requirements.txt
pip install .
playwright install

echo "Environment ready. Running tests..."
pytest