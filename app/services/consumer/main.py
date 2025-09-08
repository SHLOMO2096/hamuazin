from app.services.consumer.elastic_manager import ElasticManager
from app.services.consumer.mongo_manager import MongoManager

mongo_manager = MongoManager()
elastic_manager = ElasticManager()

mongo_manager.consume_messages_from_kafka()
elastic_manager.consume_messages_from_kafka()
