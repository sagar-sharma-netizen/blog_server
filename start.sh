#!/bin/sh
source venv/bin/activate
gunicorn -w 4 -b :9000 --access-logfile - --error-logfile - application:boot
