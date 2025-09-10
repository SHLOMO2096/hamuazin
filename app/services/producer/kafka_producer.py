from kafka import KafkaProducer
from app.log.logger import Logger
import json

logger = Logger.get_logger()

class KafkaPublisher:
    """
    Publisher for sending messages to a Kafka topic.
    """
    def __init__(self, kafka_broker: str, kafka_topic: str):
        self.kafka_topic = kafka_topic
        self.producer = KafkaProducer(
            bootstrap_servers=kafka_broker,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )
    
    def publish(self, message: dict):
        """
        Publish a message to the Kafka topic.
        """
        self.producer.send(self.kafka_topic, value=message)
        logger.info(f"Published message to Kafka topic '{self.kafka_topic}': {message}")

    def __del__(self):
        """
        Destructor for KafkaPublisher.
        """
        if hasattr(self, 'producer'):
            logger.info(f"Closing Kafka producer for topic '{self.kafka_topic}'")
            self.producer.flush()
            logger.info(f"Closed Kafka producer for topic '{self.kafka_topic}'")
            self.producer.close()