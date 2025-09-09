import config
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
        print("Consumer started listening to Kafka...")
        logger.info("Consumer started listening to Kafka...")
        try:
            for message in self.kafka_consumer.listen():
                print(f"Received message: {message}")
                logger.info(f"Received message: {message}")
                audio_path = config.AUDIO_PATH + message.get('path')
                if audio_path:
                    uuid = self.file_uuid(audio_path)
                    file_id = self.save_audio_minimal(audio_path)
                    doc = {
                        "file_id": bson.ObjectId(file_id),
                        "uuid": uuid,
                    }
                    self.send_to_mongo(doc)
                else:
                    print("No audio path found in message.")
                    logger.warning("No audio path found in message.")
        except Exception as e:
            print(f"Error consuming saving: {e}")
            logger.error(f"Error consuming saving: {e}")

    def send_to_mongo(self, doc):
        try:
            self.mongo_handler.insert_document(doc)
            print(f"Saved to Mongo: {doc}")
            logger.info(f"Saved to Mongo: {doc}")
        except Exception as e:
            print(f"MongoDB error: {e}")
            logger.error(f"MongoDB error: {e}")

    @staticmethod
    def file_uuid(path):
        stat = os.stat(path)
        data = f"{os.path.basename(path)}-{stat.st_size}-{stat.st_mtime}"
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, data))

    def save_audio_minimal(self, path):
        db = self.mongo_handler.db
        fs = GridFS(db)
        with open(path, "rb") as f:
            file_id = fs.put(f)
        return file_id


if __name__ == "__main__":
    manager = MongoManager()
    manager.consume_messages_from_kafka()