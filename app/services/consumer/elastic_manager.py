import config
import bson
import math
import uuid, os
from kafka_consumer import KafkaSubscriber
from elastic_client import ElasticSearchClient
from app.log.logger import Logger

logger = Logger.get_logger()

class ElasticManager:
    def __init__(self):
        self.kafka_consumer = KafkaSubscriber(
            config.KAFKA_TOPIC,
            config.KAFKA_ELASTIC_GROUP,
        )
        self.elastic_client = ElasticSearchClient(config.ES_HOST, config.ES_INDEX)

    def consume_messages_from_kafka(self):
        logger.info("Consumer started listening to Kafka...")
        print("Consumer started listening to Kafka...")
        try:
            for message in self.kafka_consumer.listen():
                logger.info(f"Received message: {message}")
                print(f"Received message: {message}")
                audio_path = config.AUDIO_PATH + message.get('file_path')
                if audio_path:
                    uuid = self.file_uuid(audio_path)
                    doc = {
                        **message,
                        "uuid": uuid,
                    }
                    self.send_to_elastic(doc)
                else:
                    print("No audio path found in message.")
                    logger.warning("No audio path found in message.")
        except Exception as e:
            print(f"Error consuming saving: {e}")
            logger.error(f"Error consuming saving: {e}")


    def send_to_elastic(self, doc):
        try:
            clean_doc = self.prepare_for_elastic(doc)
            self.elastic_client.save_transcription(clean_doc)
            print(f"Saved to Elastic: {clean_doc}")
        except Exception as e:
            print(f"Elastic error: {e}")


    def prepare_for_elastic(self, doc):
        doc_clean = {}
        for k, v in doc.items():
            if k == "_id":
                continue  
            elif isinstance(v, float) and math.isnan(v):
                doc_clean[k] = None
            elif isinstance(v, bson.ObjectId):
                doc_clean[k] = str(v)
            else:
                doc_clean[k] = v
        return doc_clean


    def file_uuid(self,path):
        stat = os.stat(path)
        data = f"{os.path.basename(path)}-{stat.st_size}-{stat.st_mtime}"
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, data))






if __name__ == "__main__":
    manager = ElasticManager()
    manager.consume_messages_from_kafka()