FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./service-a ./service-a
COPY ./service-b ./service-b
CMD ["uvicorn", "service-a.app:app", "--host", "0.0.0.0", "--port", "8000"]
