# src/kafka_monitor.py
###########################################################################
# File: kafka_monitor.py                                                  #
# Description: Monitors Kafka topics for domain processing.               #
# Author: cqllum                                                          #
# Date: 2024-10-23                                                        #
###########################################################################

import json
import time
from confluent_kafka import Consumer, Producer, KafkaError
from urllib.parse import urlparse
from datetime import datetime
from src.main import main   

# Load configuration from the JSON file
def load_config(filename='config/config.json'):
    with open(filename, 'r') as config_file:
        return json.load(config_file)

config = load_config()

KAFKA_BROKER = config['kafka']['brokers'][0]
PENDING_TOPIC = config['kafka']['pending_topic']
COMPLETED_TOPIC = config['kafka']['completed_topic']

def create_kafka_consumer():
    """Creates a kafka consumer."""
    return Consumer({
        'bootstrap.servers': KAFKA_BROKER,
        'group.id': 'domain-monitor-group',
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': True,
        'security.protocol': config['kafka']['security_protocol'],
        'sasl.mechanisms': config['kafka']['sasl_mechanisms'],
        'sasl.username': config['kafka']['sasl_username'],
        'sasl.password': config['kafka']['sasl_password']
    })

def create_kafka_producer():
    """Creates a kafka producer."""

    return Producer({
        'bootstrap.servers': KAFKA_BROKER,
        'security.protocol': config['kafka']['security_protocol'],
        'sasl.mechanisms': config['kafka']['sasl_mechanisms'],
        'sasl.username': config['kafka']['sasl_username'],
        'sasl.password': config['kafka']['sasl_password']
    })

def is_valid_url(url):
    """Check if the provided URL has a valid scheme and netloc."""
    parsed = urlparse(url)
    return all([parsed.scheme, parsed.netloc])

def serialize_data(data):
    """Recursively convert datetime objects to ISO format strings."""
    if isinstance(data, dict):
        return {key: serialize_data(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [serialize_data(item) for item in data]
    elif isinstance(data, datetime):
        return data.isoformat()
    return data

def process_message(msg, processed_urls, producer):
    """Process a single Kafka message."""
    message_value = msg.value().decode('utf-8')
    print(f"Raw message received: {message_value}")

    try:
        domain_data = json.loads(message_value)
        domain = domain_data.get('domain')
    except json.JSONDecodeError:
        domain = message_value

    if not domain or 'cloudflare' in domain:
        print(f"Skipping domain: {domain}")
        return

    if domain in processed_urls:
        print(f"Skipping already processed domain: {domain}")
        return

    print(f"Processing domain: {domain}")
    processed_urls.add(domain)
    results = main(domain)

    if not results.get('success', False):
        print(f"Failed to process {domain}: {results.get('error', 'Unknown error')}")
        return

    producer.produce(COMPLETED_TOPIC, json.dumps(results).encode('utf-8'))
    print(f"Results for {domain} sent to {COMPLETED_TOPIC}")

    handle_internal_links(results.get('internal_links', []), processed_urls, producer)

def handle_internal_links(internal_links, processed_urls, producer):
    """Handle internal links from the processed domain results."""
    for link in internal_links:
        if link not in processed_urls:
            producer.produce(PENDING_TOPIC, link.encode('utf-8'))
            print(f"New link added to pending analysis: {link}")

def process_domains():
    consumer = create_kafka_consumer()
    producer = create_kafka_producer()
    consumer.subscribe([PENDING_TOPIC])
    processed_urls = set()

    while True:
        try:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                print(f"Error: {msg.error()}")
                break

            process_message(msg, processed_urls, producer)
            time.sleep(0.1)  # Optional delay

        except Exception as e:
            print(f"An error occurred: {e}")

    consumer.close()

if __name__ == "__main__":
    print("Listening for new domains to process...")
    process_domains()
