FROM python:3.13-slim

WORKDIR /app

ARG APP_ENV=dev

COPY requirements.txt .
COPY requirements-dev.txt .
RUN if [ "$APP_ENV" = "prod" ]; then \
      pip install --no-cache-dir -r requirements.txt; \
    else \
      apt-get update && apt-get install -y --no-install-recommends libgomp1 && rm -rf /var/lib/apt/lists/* && \
      pip install --no-cache-dir -r requirements-dev.txt; \
    fi

COPY . .

ENV PYTHONPATH=/app/src
ENV APP_ENV=${APP_ENV}
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
