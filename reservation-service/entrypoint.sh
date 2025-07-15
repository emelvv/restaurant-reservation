#!/bin/sh
set -e

# Ждём, пока postgres будет готов
until pg_isready -h "${POSTGRES_HOST:-postgres}" -p 5432 -U "${POSTGRES_USER:-user}"; do
  echo "Waiting for postgres…"
  sleep 2
done

# Заполняем БД данными
python app/seed_data.py

# Запускаем FastAPI
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
