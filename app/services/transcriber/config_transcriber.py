import os


MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "podcasts")
MONGO_DB = os.getenv("MONGO_DB", "podcasts_db")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
ES_HOST = os.getenv("ELASTIC_URI", "http://localhost:9200")
ES_INDEX = os.getenv("ES_INDEX", "podcasts")