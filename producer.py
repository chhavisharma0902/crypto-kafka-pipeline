from kafka import KafkaProducer
import json
import time
import random

# Kafka broker URL
KAFKA_BROKER = 'localhost:9092'
TOPIC = 'crypto-topic'

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',  # <-- must match Docker port mapping
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

cryptos = ['BTC', 'ETH', 'SOL', 'ADA']

try:
    while True:
        data = {
            "coin": random.choice(cryptos),
            "price": round(random.uniform(10, 50000), 2),
            "timestamp": int(time.time())
        }
        producer.send(TOPIC, value=data)
        print(f"Sent: {data}")
        time.sleep(2)  # send every 2 seconds
except KeyboardInterrupt:
    print("Stopping producer...")
finally:
    producer.close()
