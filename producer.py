import os
import json
import time
import random
import requests
from kafka import KafkaProducer

# === Configuration ===
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "crypto-topic")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL_SECONDS", "10"))
USE_API = os.getenv("USE_API", "False").lower() == "true"  # Toggle between API and random data

# === Kafka Producer Setup ===
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

# === API URL (for live data mode) ===
API_URL = "https://api.coingecko.com/api/v3/simple/price"
CRYPTO_IDS = "bitcoin,ethereum"

print(f"[Producer] Started. Mode: {'API (CoinGecko)' if USE_API else 'Random Data'}")
print(f"[Producer] Sending data to topic: {TOPIC}")

# === Main Loop ===
while True:
    try:
        if USE_API:
            # Fetch live crypto prices from CoinGecko
            response = requests.get(API_URL, params={"ids": CRYPTO_IDS, "vs_currencies": "usd"})
            if response.status_code == 200:
                data = response.json()
                record = {"fetched_at": int(time.time()), "data": data}
                producer.send(TOPIC, record)
                producer.flush()
                print(f"[Producer] Sent (API): {record}")
            else:
                print("[Producer] Error fetching API:", response.status_code)
        else:
            # Generate random test data
            cryptos = ['BTC', 'ETH', 'SOL', 'ADA']
            record = {
                "coin": random.choice(cryptos),
                "price": round(random.uniform(10, 50000), 2),
                "timestamp": int(time.time())
            }
            producer.send(TOPIC, value=record)
            producer.flush()
            print(f"[Producer] Sent (Random): {record}")

    except Exception as e:
        print("[Producer] Error:", e)

    time.sleep(POLL_INTERVAL)
