python manage.py makemigrations api
python manage.py makemigrations jwt_auth
python manage.py migrate
python manage.py collectstatic --no-input
gunicorn --bind 0.0.0.0:8000 backend.wsgi:application
