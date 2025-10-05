import os
import json
import time
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import KafkaError, NoBrokersAvailable

# Environment variables (fallback to default if not found)
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
INPUT_TOPIC = os.getenv("INPUT_TOPIC", "api-raw-data")
OUTPUT_TOPIC = os.getenv("OUTPUT_TOPIC", "api-processed-data")

# Wait for Kafka to be ready (important in Docker Compose)
for _ in range(10):
    try:
        consumer = KafkaConsumer(
            INPUT_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        )
        break
    except NoBrokersAvailable:
        print("[Processor] Kafka not available yet, retrying...")
        time.sleep(5)
else:
    print("[Processor] Failed to connect to Kafka after several retries.")
    exit(1)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

print(f"[Processor] Connected to Kafka at {KAFKA_BOOTSTRAP}")
print(f"[Processor] Listening for messages on topic '{INPUT_TOPIC}'...")

while True:
    try:
        for msg in consumer:
            data = msg.value
            raw = data.get("raw", {})
            fetched_at = data.get("fetched_at", int(time.time()))

            for coin_id in ["bitcoin", "ethereum"]:
                if coin_id in raw:
                    price_usd = raw[coin_id].get("usd", 0.0)
                    processed = {
                        "id": coin_id,
                        "price_usd": price_usd,
                        "status": "active" if price_usd > 0 else "unknown",
                        "fetched_at": fetched_at,
                        "processed_at": int(time.time()),
                    }
                    producer.send(OUTPUT_TOPIC, processed)
                    print(f"[Processor] Sent {coin_id}: {processed}")

            producer.flush()

    except KafkaError as e:
        print(f"[Processor] Kafka error: {e}")
        time.sleep(5)
    except Exception as e:
        print(f"[Processor] Unexpected error: {e}")
        time.sleep(5)
