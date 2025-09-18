FROM python:3.11-slim
WORKDIR /sim
COPY . .
RUN pip install influxdb-client
CMD ["python","generator.py"]
