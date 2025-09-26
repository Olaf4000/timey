#!/bin/bash

# exit on error
set -e

# Create virtual environment if not exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate venv
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Start python file (replace app.py with your file)
echo "Starting application..."
python timey.py