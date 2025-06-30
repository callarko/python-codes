FROM python:3.9-slim

RUN pip install Flask

COPY webhook.py /app/webhook.py

WORKDIR /certs

# Generate a self-signed certificate
RUN openssl req -newkey rsa:2048 -nodes -keyout webhook-server.key -x509 -days 365 -out webhook-server.crt -subj "/CN=webhook-server.webhook-system.svc"

WORKDIR /app

CMD ["python", "webhook.py"]
