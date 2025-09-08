from kafka import KafkaProducer
import json

class KafkaPublisher:
    def __init__(self, kafka_broker: str, kafka_topic: str):
        self.kafka_topic = kafka_topic
        self.producer = KafkaProducer(
            bootstrap_servers=kafka_broker,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )
    
    def publish(self, message: dict):
        self.producer.send(self.kafka_topic, value=message)
        print(f"Message sent to Kafka topic '{self.kafka_topic}'")

    def __del__(self):
        if hasattr(self, 'producer'):
            self.producer.flush()
            self.producer.close()