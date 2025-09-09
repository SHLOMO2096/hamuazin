import os

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BROKER", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "podcasts")
KAFKA_MONGO_GROUP = os.getenv("KAFKA_MONGO_GROUP", "mongo_group")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "podcasts")
MONGO_DB = os.getenv("MONGO_DB", "podcasts_db")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
ES_HOST = os.getenv("ELASTIC_URI", "http://localhost:9200")
ES_INDEX = os.getenv("ES_INDEX", "podcasts")
KAFKA_ELASTIC_GROUP = os.getenv("KAFKA_ELASTIC_GROUP", "elastic_group")
# AUDIO_PATH =  "/data/clips/"