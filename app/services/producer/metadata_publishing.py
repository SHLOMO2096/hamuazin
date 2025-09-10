from pathlib import Path
import json
from kafka_producer import KafkaPublisher
from app.log.logger import Logger
import time

logger = Logger.get_logger()

class Metadata_publishing:
    """
    Class to publish file metadata to a Kafka topic.
    """
    def __init__(self, kafka_producer: KafkaPublisher, path: str):
        self.kafka_producer = kafka_producer
        self.path = path

    def get_file_metadata(self, file_path: Path):
        """
        Get metadata for a file.
        """
        return {
            "file_path": file_path,
            "name": file_path.name,
            "size": file_path.stat().st_size,
            "created": file_path.stat().st_ctime,
            "modified": file_path.stat().st_mtime,
            "suffix": file_path.suffix
        }

    def sending_to_kafka(self):
        """
          Continuously monitor the directory and send metadata of new files to Kafka.
        """
        processed_files = set()
        while True:
            for file in Path(self.path).glob('*'):
                if file.is_file() and str(file) not in processed_files:
                    metadata = self.get_file_metadata(file)
                    json_metadata = json.dumps(metadata)
                    self.kafka_producer.publish(json_metadata)
                    logger.info(json_metadata)
                    logger.info(f"Sent metadata for {file.name} to Kafka")
                    processed_files.add(str(file))
            time.sleep(10)


if __name__ == "__main__":
    logger = Logger.get_logger()
    kafka_producer = KafkaPublisher(kafka_broker="localhost:9092", kafka_topic="podcasts")
    producer = Metadata_publishing(kafka_producer=kafka_producer, path="C:\\Users\\shlomo\\Downloads\\podcasts\\download (28).wav")
    logger.info("Starting to send metadata to Kafka topic 'podcasts'")
    print(type(producer.get_file_metadata(Path("C:\\Users\\shlomo\\Downloads\\podcasts\\download (28).wav"))))