import config
import json
import bson
import math
import uuid, os
from kafka_consumer import KafkaSubscriber
from elastic_client import ElasticSearchClient
from app.log.logger import Logger

logger = Logger.get_logger()

class ElasticManager:
    """
    Manager to consume messages from Kafka and index them into Elasticsearch.
    """
    def __init__(self):
        self.kafka_consumer = KafkaSubscriber(
            config.KAFKA_TOPIC,
            config.KAFKA_ELASTIC_GROUP,
        )
        self.elastic_client = ElasticSearchClient(config.ES_HOST, config.ES_INDEX)

    def consume_messages_from_kafka(self):
        """
        Start consuming messages from Kafka.
        """
        logger.info("Consumer_elastic started listening to Kafka...")
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
                    doc = {
                        **msg,
                        "uuid": f_uuid,
                    }
                    self.send_to_elastic(doc)
                else:
                    logger.warning("No audio path found in message.")
        except Exception as e:
            logger.error(f"Error consuming saving: {e}")


    def send_to_elastic(self, doc):
        """
        Send a document to Elasticsearch.
        """
        try:
            clean_doc = self.prepare_for_elastic(doc)
            self.elastic_client.save_transcription(clean_doc)
            logger.info(f"Saved to Elastic: {clean_doc}")
        except Exception as e:
            logger.error(f"Elastic error: {e}")


    def prepare_for_elastic(self, doc):
        """
        Prepare document for Elasticsearch by cleaning it.
        """
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


    def file_uuid(self, path):
        """
        Generate a UUID for the given file path.
        """
        stat = os.stat(path)
        data = f"{os.path.basename(path)}-{stat.st_size}-{stat.st_mtime}"
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, data))






if __name__ == "__main__":
    manager = ElasticManager()
    manager.consume_messages_from_kafka()