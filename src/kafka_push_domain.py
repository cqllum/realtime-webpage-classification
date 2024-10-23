# src/kafka_push_domain.py
##########################################################################
# File: kafka_push_domain.py                                             #
# Description: Sends domains to Kafka for processing.                    #
# Author: cqllum                                                         #
# Date: 2024-10-23                                                       #
##########################################################################

import json
import argparse
from confluent_kafka import Producer

def load_config(filename='config/config.json'):
    """Load configuration from a JSON file."""
    with open(filename, 'r') as config_file:
        return json.load(config_file)

def create_kafka_producer(config):
    """Create and return a Kafka producer."""
    return Producer({
        'bootstrap.servers': config['kafka']['brokers'][0],
        'sasl.mechanisms': config['kafka']['sasl_mechanisms'],
        'security.protocol': config['kafka']['security_protocol'],
        'sasl.username': config['kafka']['sasl_username'],
        'sasl.password': config['kafka']['sasl_password']
    })

def send_domain(domain, producer, topic):
    """Send a domain to the specified Kafka topic."""
    message = json.dumps({'domain': domain}).encode('utf-8')
    producer.produce(topic, value=message)
    producer.flush()
    print(f"Domain {domain} sent to {topic}")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Send domain to Kafka topic')
    parser.add_argument('--domain', required=True, help='Domain to send to Kafka topic')
    args = parser.parse_args()

    # Load the configuration
    config = load_config()

    # Create Kafka producer
    producer = create_kafka_producer(config)

    # Send the provided domain
    send_domain(args.domain, producer, config['kafka']['pending_topic'])

if __name__ == "__main__":
    main()
