web: gunicorn PLANEKS.wsgi --log-file -
celery: celery -A celery_tasks worker -c 2 -l info
