web: gunicorn PLANEKS.wsgi --log-file -
celery: celery -A celery_tasks worker -c 2 -l info & celery -A celery_tasks beat --scheduler django_celery_beat.schedulers:DatabaseScheduler

