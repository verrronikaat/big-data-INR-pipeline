# kafka/consumer_hdfs.py
from kafka import KafkaConsumer
import json
import subprocess
from datetime import datetime
import os
import logging
import signal
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

running = True

def signal_handler(sig, frame):
    global running
    logger.info("🛑 Shutting down consumer...")
    running = False

signal.signal(signal.SIGINT, signal_handler)

def save_to_hdfs(data, source):
    """Сохранение сообщения в HDFS"""
    date_str = datetime.now().strftime('%Y-%m-%d')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    filename = f"data_{timestamp}.json"
    hdfs_path = f"/user/cloudera/raw_data/source={source}/date={date_str}/{filename}"
    
    # Временный локальный файл
    local_path = f"C:\\temp\\{filename}"
    os.makedirs("C:\\temp", exist_ok=True)
    
    try:
        with open(local_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
        
        # Пытаемся скопировать в HDFS
        # Для Windows нужно настроить hdfs команду или использовать другой подход
        result = subprocess.run(['hdfs', 'dfs', '-mkdir', '-p', f'/user/cloudera/raw_data/source={source}/date={date_str}'], 
                              capture_output=True, text=True, shell=True)
        result2 = subprocess.run(['hdfs', 'dfs', '-put', '-f', local_path, hdfs_path], 
                               capture_output=True, text=True, shell=True)
        
        os.remove(local_path)
        
        if result2.returncode == 0:
            logger.info(f"✅ Saved to HDFS: {hdfs_path}")
        else:
            logger.error(f"❌ Failed to save: {result2.stderr}")
    except Exception as e:
        logger.error(f"❌ Error saving to HDFS: {e}")

def main():
    """Основная функция consumer"""
    try:
        consumer = KafkaConsumer(
            'raw-data',
            bootstrap_servers='localhost:9092',
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        logger.info("✅ Consumer connected to Kafka")
        logger.info("📡 Waiting for messages... Press Ctrl+C to stop")
        
        for msg in consumer:
            if not running:
                break
            data = msg.value
            source = data.get('source', 'unknown')
            logger.info(f"📨 Received: source={source}, rate={data.get('rate')}")
            save_to_hdfs(data, source)
        
        consumer.close()
    except Exception as e:
        logger.error(f"❌ Consumer error: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("📀 Kafka Consumer → HDFS")
    print("=" * 50)
    main()