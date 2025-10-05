import os
import json
import time
from kafka import KafkaConsumer
from pymongo import MongoClient

# === Configuration ===
# Automatically switch between Docker and local environments
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "crypto-topic")

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB = os.getenv("MONGO_DB", "crypto_db")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "crypto_data")

# === Kafka Consumer Setup ===
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="crypto-group",
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
)

# === MongoDB Connection ===
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[MONGO_DB]
collection = db[MONGO_COLLECTION]

print(f"[Consumer] Started. Listening for messages on topic '{TOPIC}'...")

# === Message Processing Loop ===
while True:
    try:
        for msg in consumer:
            record = msg.value
            collection.insert_one(record)
            print(f"[Consumer] Inserted into MongoDB: {record}")
    except Exception as e:
        print("[Consumer] Error:", e)
        time.sleep(5)
