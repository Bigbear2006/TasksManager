python manage.py migrate
python manage.py collectstatic --no-input
gunicorn --bind 0.0.0.0:8000 backend.wsgi:application
