from metadata_publishing import Metadata_publishing
from kafka_producer import KafkaPublisher
from app.log.logger import Logger
import config_producer


if __name__ == "__main__":
    logger = Logger.get_logger()
    kafka_producer = KafkaPublisher(kafka_broker=config_producer.KAFKA_BOOTSTRAP, kafka_topic=config_producer.KAFKA_TOPIC)
    producer = Metadata_publishing(kafka_producer=kafka_producer, path=config_producer.PATH)
    logger.info(f"Starting to send metadata from {config_producer.PATH} to Kafka topic {config_producer.KAFKA_TOPIC}")
    producer.sending_to_kafka()
    