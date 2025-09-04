import os
import json
import time
from confluent_kafka import Consumer
import psycopg2
import redis

def load_kafka_consumer():
    consumer = Consumer({
        'bootstrap.servers': os.environ.get("KAFKA_BOOTSTRAP_SERVERS"),
        'group.id': 'event_processor_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe(['multimedia_events'])
    return consumer

def connect_postgres():
    return psycopg2.connect(
        host=os.environ.get("POSTGRES_HOST"),
        dbname=os.environ.get("POSTGRES_DB"),
        user=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD")
    )

def connect_redis():
    return redis.Redis(
        host=os.environ.get("REDIS_HOST"),
        db=int(os.environ.get("REDIS_DB", "0")),
        decode_responses=True
    )

def process_event(msg, cur, r):
    data = json.loads(msg.value().decode('utf-8'))
    enriched = {
        "event_id": data["event_id"],
        "user_id": data["user_id"],
        "content": data["content"],
        "timestamp": data["timestamp"],
        "processed_at": int(time.time())
    }
    cur.execute(
        "INSERT INTO events (event_id, user_id, content, timestamp, processed_at) VALUES (%s, %s, %s, %s, %s)",
        (enriched["event_id"], enriched["user_id"], enriched["content"], enriched["timestamp"], enriched["processed_at"])
    )
    r.set(f"{os.environ.get('REDIS_KEY_PREFIX')}:{enriched['event_id']}", json.dumps(enriched))

def main():
    consumer = load_kafka_consumer()
    conn = connect_postgres()
    cur = conn.cursor()
    r = connect_redis()
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue
            process_event(msg, cur, r)
            conn.commit()
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
        cur.close()
        conn.close()

if __name__ == "__main__":
    main()
