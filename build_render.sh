#!/usr/bin/env bash
# Build script for Render deployment

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Setting Render environment variables..."
export RENDER=true
export DEBUG=false
export ALLOWED_HOSTS="*"

echo "Build completed!"
