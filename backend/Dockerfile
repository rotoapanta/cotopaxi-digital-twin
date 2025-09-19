# backend/Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir fastapi uvicorn influxdb-client pydantic pydantic-settings
CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8000"]
