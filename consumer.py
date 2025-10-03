from kafka import KafkaConsumer
import json
from pymongo import MongoClient

# Kafka setup
consumer = KafkaConsumer(
    'crypto-topic',  # Replace with your topic name
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='crypto-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['crypto_db']        # Database name
collection = db['crypto_data']  # Collection name

print("Consumer is running and listening to messages...")

for message in consumer:
    data = message.value
    print(f"Received: {data}")

    # Insert into MongoDB
    collection.insert_one(data)
    print("Saved to MongoDB")
