#!/bin/sh
set -e

# Ждём, пока Postgres будет готов
until pg_isready -h postgres -p 5432 -U user; do
  echo "Waiting for postgres..."
  sleep 2
done

# Затем запускаем uvicorn
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
