# Real-Time Cryptocurrency Data Pipeline 🚀

This project demonstrates a **real-time data pipeline** using **Kafka, Zookeeper, MongoDB, and Python**.  
It fetches live cryptocurrency prices from the **CoinGecko API**, processes them with Kafka, and stores the results in MongoDB — all running locally with Docker.

---

## 📂 Project Structure

crypto-kafka-pipeline/
├─ docker-compose.yml # Defines all services
├─ producer/ # Fetches data from CoinGecko and sends to Kafka
│ ├─ producer.py
│ └─ Dockerfile
├─ processor/ # Processes raw data and publishes to a new Kafka topic
│ ├─ processor.py
│ └─ Dockerfile
├─ consumer/ # Reads processed data and stores in MongoDB
│ ├─ consumer.py
│ └─ Dockerfile


---

## ⚙️ Components

- **Zookeeper** – Coordinates Kafka brokers  
- **Kafka** – Messaging backbone with topics:
  - `api-raw-data` (raw data from API)
  - `api-processed-data` (filtered + enriched data)
- **Producer (Python)** – Pulls live data from CoinGecko API every 10 seconds  
- **Processor (Python)** – Filters for Bitcoin & Ethereum, adds timestamp/status  
- **Consumer (Python)** – Inserts processed data into MongoDB  
- **MongoDB** – Stores the results for querying/analysis  

---

## 🛠️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/crypto-kafka-pipeline.git
cd crypto-kafka-pipeline
