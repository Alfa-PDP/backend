# file gunicorn.conf.py
# coding=utf-8

import multiprocessing
import os

loglevel = os.environ.get("GUNICORN_LOG_LEVEL", "info")
errorlog = "-"
accesslog = "-"

bind = f'{os.environ.get("PROJECT_HOST", "127.0.0.1")}:{os.environ.get("PROJECT_PORT", 8080)}'

workers = multiprocessing.cpu_count() * 2 + 1

timeout = 3 * 60  # 3 minutes
keepalive = 24 * 60 * 60  # 1 day

worker_class = "uvicorn.workers.UvicornWorker"
