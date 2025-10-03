import os
import json
import time
from kafka import KafkaConsumer
from pymongo import MongoClient

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
TOPIC = "api-processed-data"

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017")
MONGO_DB = os.getenv("MONGO_DB", "crypto_db")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "prices")

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
)

mongo_client = MongoClient(MONGO_URI)
db = mongo_client[MONGO_DB]
collection = db[MONGO_COLLECTION]

print("[Consumer] Started. Listening for processed data...")

while True:
    try:
        for msg in consumer:
            record = msg.value
            collection.insert_one(record)
            print(f"[Consumer] Inserted into MongoDB: {record}")
    except Exception as e:
        print("[Consumer] Error:", e)
        time.sleep(5)
