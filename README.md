# Global Event Streaming Platform for Multimedia Data

This project demonstrates a containerized streaming platform built with Kafka and a Python event processor. The platform is capable of ingesting, processing, and enriching multimedia event messages at scale while persisting records to both PostgreSQL and Redis for hybrid transactional and concurrent query workloads. The goal of this architecture is to achieve low-latency processing for millions of events per day and maintain high uptime under peak global traffic.

## Architecture Overview

The system consists of the following components:

- **Kafka** — A distributed event streaming platform used to ingest and publish multimedia event messages. Topics are automatically created and configured for partitioning and replication.
- **Zookeeper** — Used by Kafka to manage cluster metadata.
- **PostgreSQL** — A relational database for durable storage of processed event data.
- **Redis** — An in‑memory data store used as a cache for fast lookups of recent or frequently accessed events.
- **Processor** — A Python service that consumes events from Kafka, performs enrichment logic, writes records to PostgreSQL, and updates Redis.

All services are orchestrated via Docker Compose. When the stack is running, you can publish JSON messages to the `multimedia_events` topic, and the processor will consume and persist them. The sample processor demonstrates how to handle streaming ingestion and writes to both transactional storage and a high‑throughput cache.

## Running the Project

1. Ensure [Docker](https://docs.docker.com/get-docker/) is installed on your system.
2. Navigate to the project directory and start the services:

   ```sh
   docker compose up --build
   ```

3. Once the stack is running, you can produce test messages to Kafka using the Kafka client tools or any Kafka client library. For example, using the Bitnami Kafka image:

   ```sh
   docker exec -it $(docker ps -qf "ancestor=bitnami/kafka:3.5") kafka-console-producer.sh \
     --bootstrap-server localhost:9092 --topic multimedia_events
   {
     "id": "event1",
     "timestamp": "2025-08-31T12:00:00Z",
     "type": "video_view",
     "user": "user123",
     "metadata": {"quality": "1080p"}
   }
   ```

4. The processor will consume the messages, insert them into the `events` table in PostgreSQL, and store them in Redis with keys like `event:<id>`.

## Customization

- To change the Kafka topic name, set the `KAFKA_TOPIC` environment variable in the `processor` service definition.
- The processor can be extended to perform additional enrichment logic or write to other storage backends.

## License

This project is released under the MIT License.
