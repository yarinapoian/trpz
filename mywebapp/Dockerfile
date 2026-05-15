FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY models.py .
COPY service.py .
COPY migrate.py .

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

ENV APP_HOST=0.0.0.0
ENV APP_PORT=3000
ENV DB_HOST=database
ENV DB_USER=app
ENV DB_PASSWORD=app
ENV DB_NAME=task_tracker

CMD ["sh", "-c", "python migrate.py --host $DB_HOST --user $DB_USER --password $DB_PASSWORD --database $DB_NAME && python app.py --host $APP_HOST --port $APP_PORT --db-host $DB_HOST --db-user $DB_USER --db-password $DB_PASSWORD --db-name $DB_NAME"]