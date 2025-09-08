from pathlib import Path
import json
from KafkaPublisher import KafkaPublisher
from app.log.logger import Logger
import time

logger = Logger.get_logger()

class Metadata_publishing:
    def __init__(self, kafka_producer: KafkaPublisher, path: str):
        self.kafka_producer = kafka_producer
        self.path = path

    def get_file_metadata(self, file_path: Path):
        return {
            "file_path": str(file_path),
            "name": file_path.name,
            "size": file_path.stat().st_size,
            "created": file_path.stat().st_birthtime, #st_ctime
            "modified": file_path.stat().st_mtime,
            "suffix": file_path.suffix
        }

    def sending_to_kafka(self):
        processed_files = set()
        while True:
            for file in Path(self.path).glob('*'):
                if file.is_file() and str(file) not in processed_files:
                    metadata = self.get_file_metadata(file)
                    json_metadata = json.dumps(metadata)
                    self.kafka_producer.publish(json_metadata)
                    print(f"Sent metadata for {file.name} to Kafka")
                    logger.info(f"Sent metadata for {file.name} to Kafka")
                    processed_files.add(str(file))
            time.sleep(10)


