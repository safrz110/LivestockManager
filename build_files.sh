# Build script for Vercel
echo "Building the project..."
python -m pip install -r requirements.txt
python manage.py collectstatic --noinput
echo "Build completed successfully!"
