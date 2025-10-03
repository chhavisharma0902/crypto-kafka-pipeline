import os
import json
import time
from kafka import KafkaConsumer, KafkaProducer

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
INPUT_TOPIC = "api-raw-data"
OUTPUT_TOPIC = "api-processed-data"

consumer = KafkaConsumer(
    INPUT_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

print("[Processor] Started. Listening for raw data...")

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
                    producer.flush()
                    print(f"[Processor] Sent {coin_id}: {processed}")
    except Exception as e:
        print("[Processor] Error:", e)
        time.sleep(5)
