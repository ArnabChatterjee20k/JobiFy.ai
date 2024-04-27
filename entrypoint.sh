#!/bin/bash

celery -A celery_worker.celery_app worker --loglevel INFO -P solo &

exec "$@"