#!/bin/bash
# Run script for the dashboard

echo "Starting dashboard..."
echo "Installing packages..."

pip install -r requirements.txt

echo "Dashboard will be at: http://127.0.0.1:8050"

cd app
python main.py
