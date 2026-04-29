# kafka/batch_producer.py
import pandas as pd
import json
import time
from kafka import KafkaProducer
from datetime import datetime
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_producer():
    """Создание подключения к Kafka"""
    try:
        producer = KafkaProducer(
            bootstrap_servers='192.168.0.163:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            retries=3
        )
        logger.info("✅ Producer connected to Kafka")
        return producer
    except Exception as e:
        logger.error(f"❌ Failed to connect to Kafka: {e}")
        return None

def send_rates(producer, topic='raw-data'):
    """Отправка курсов из CSV в Kafka"""
    csv_path = 'dataset/dataset.csv'
    
    if not os.path.exists(csv_path):
        logger.error(f"❌ File not found: {csv_path}")
        return
    
    df = pd.read_csv(csv_path)
    logger.info(f"📊 Loaded {len(df)} records from {csv_path}")
    
    sent_count = 0
    for _, row in df.iterrows():
        message = {
            'source': 'batch',
            'timestamp': row['date'],
            'rate': float(row['rate']),
            'currency': 'INR'
        }
        
        try:
            future = producer.send(topic, value=message)
            record_metadata = future.get(timeout=10)
            sent_count += 1
            logger.info(f"✅ Sent [{sent_count}]: {message['timestamp']} -> {message['rate']}")
        except Exception as e:
            logger.error(f"❌ Failed to send: {e}")
        
        time.sleep(0.1)  # небольшая задержка
    
    logger.info(f"🎉 Done! Sent {sent_count} messages to topic '{topic}'")
    return sent_count

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 Batch Producer for INR Currency Rates")
    print("=" * 50)
    
    producer = create_producer()
    if producer:
        send_rates(producer)
        producer.flush()
        producer.close()
        logger.info("Producer closed")