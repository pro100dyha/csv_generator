#!/usr/bin/env bash
celery -A celery_tasks worker -c 2 -l info