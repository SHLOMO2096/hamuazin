import config
import json
import bson
from gridfs import GridFS
import uuid, os
from kafka_consumer import KafkaSubscriber
from mongo_client import MongoHandler
from app.log.logger import Logger

logger = Logger.get_logger()

class MongoManager:
    def __init__(self):
        self.kafka_consumer = KafkaSubscriber(
            config.KAFKA_TOPIC,
            config.KAFKA_MONGO_GROUP
        )
        self.mongo_handler = MongoHandler(config.MONGO_URI, config.MONGO_DB, config.MONGO_COLLECTION)

    def consume_messages_from_kafka(self):
        global payload
        logger.info("Consumer_mongo started listening to Kafka...")
        try:
            for message in self.kafka_consumer.listen():
                logger.info(f"Received message: {message}")
                if hasattr(message, "value"):
                    payload = message.value
                else:
                    payload = message

                if isinstance(payload, bytes):
                    payload = payload.decode("utf-8")

                if isinstance(payload, str):
                    try:
                        msg = json.loads(payload)
                    except Exception as e:
                        logger.error(f"Invalid JSON: {e} | payload={payload}")
                        continue
                elif isinstance(payload, dict):
                    msg = payload
                else:
                    logger.error(f"Unexpected payload type: {type(payload)}")
                    continue

                audio_path = msg.get("file_path")
                if audio_path:
                    f_uuid = self.file_uuid(audio_path)
                    file_id = self.save_audio_minimal(audio_path)
                    doc = {
                        "file_id": file_id,
                        "uuid": f_uuid,
                    }
                    self.send_to_mongo(doc)
                else:
                    logger.warning("No audio path found in message.")
        except Exception as e:
            logger.error(f"Error consuming saving: {e}")

    def send_to_mongo(self, doc):
        try:
            self.mongo_handler.insert_document(doc)
            logger.info(f"Saved to Mongo: {doc}")
        except Exception as e:
            print(f"MongoDB error: {e}")
            logger.error(f"MongoDB error: {e}")

    @staticmethod
    def file_uuid(path):
        """
        Generate a UUID for the given file path.
        """
        stat = os.stat(path)
        data = f"{os.path.basename(path)}-{stat.st_size}-{stat.st_mtime}"
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, data))

    def save_audio_minimal(self, path):
        """
        Save audio file to MongoDB GridFS and return the file ID.
        """
        db = self.mongo_handler.db
        fs = GridFS(db)
        with open(path, "rb") as f:
            file_id = fs.put(f)
        return file_id


if __name__ == "__main__":
    manager = MongoManager()
    manager.consume_messages_from_kafka()