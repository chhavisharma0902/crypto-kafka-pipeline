import os
import json
import time
import requests
from kafka import KafkaProducer

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
TOPIC = "api-raw-data"
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL_SECONDS", "10"))

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

API_URL = "https://api.coingecko.com/api/v3/simple/price"

print("[Producer] Started. Fetching data from CoinGecko...")

while True:
    try:
        response = requests.get(API_URL, params={"ids": "bitcoin,ethereum", "vs_currencies": "usd"})
        if response.status_code == 200:
            data = response.json()
            record = {"fetched_at": int(time.time()), "raw": data}
            producer.send(TOPIC, record)
            producer.flush()
            print(f"[Producer] Sent: {record}")
        else:
            print("[Producer] Error fetching API:", response.status_code)
    except Exception as e:
        print("[Producer] Error:", e)
    time.sleep(POLL_INTERVAL)
