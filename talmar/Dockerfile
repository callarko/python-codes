# Use a lightweight Python image
FROM python:3.10-slim

# Install dependencies
RUN pip install fastapi uvicorn cryptography

# Copy app code
COPY app.py /app/app.py
WORKDIR /app

# Expose the port
EXPOSE 8080

# Start FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
