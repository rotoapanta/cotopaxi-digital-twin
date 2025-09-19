FROM python:3.11-slim
WORKDIR /sim
COPY . .
RUN pip install --no-cache-dir influxdb-client
CMD ["python","generator.py"]
