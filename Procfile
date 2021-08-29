web: gunicorn PLANEKS.wsgi --log-file -
celery: celery worker -A celery_tasks -l info -c 4

