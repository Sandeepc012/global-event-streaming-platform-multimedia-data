FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY processor.py .
ENV KAFKA_BOOTSTRAP_SERVERS=kafka:9092
ENV POSTGRES_HOST=postgres
ENV POSTGRES_DB=multimedia
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV REDIS_HOST=redis
ENV REDIS_DB=0
ENV REDIS_KEY_PREFIX=multimedia
CMD ["python","processor.py"]
