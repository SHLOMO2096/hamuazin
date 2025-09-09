from mongo_client import MongoHandler
from elastic_client import ElasticSearchClient
from faster_whisper import WhisperModel

class TranscriberManager:
    def __init__(self, mongo_uri, mongo_db, mongo_collection, es_host):
        self.mongo_handler = MongoHandler(mongo_uri, mongo_db, mongo_collection)
        self.es_client = ElasticSearchClient(es_host)
        self.whisper_model = WhisperModel("base") 
        self.model = WhisperModel("base", device="cpu", compute_type="int8")

