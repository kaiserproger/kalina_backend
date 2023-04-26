#!/usr/bin/env bash

set -e

DEFAULT_MODULE_NAME=main

MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-src}
export src_MODULE=${src_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-80}
LOG_LEVEL=${LOG_LEVEL:-info}
LOG_CONFIG=${LOG_CONFIG:-/src/logging.ini}

# Start Uvicorn with live reload
poetry shell
alembic upgrade head
exec uvicorn --reload --proxy-headers --host $HOST --port $PORT --log-config $LOG_CONFIG "$src_MODULE"
