FROM python:3.12-slim

WORKDIR /app

COPY app.py /app

CMD ["python3", "/app/app.py"]
