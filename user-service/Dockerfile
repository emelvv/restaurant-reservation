FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
       postgresql-client \
       gcc \
       libpq-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8000

ENV DATABASE_URL="postgresql://user:pass@postgres:5432/bookingdb"

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
