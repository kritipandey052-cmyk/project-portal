release: python manage.py collectstatic --noinput && python manage.py migrate
web: gunicorn dashboard_portal.wsgi
