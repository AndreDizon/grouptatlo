web: cd backend && gunicorn parking_system.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 120
release: cd backend && python manage.py migrate && python manage.py collectstatic --noinput
