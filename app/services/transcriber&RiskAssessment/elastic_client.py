import os
from elasticsearch import Elasticsearch
from app.log.logger import Logger
import config_transcriber

logger = Logger.get_logger()

class ElasticSearchClient:
    """
    Client for interacting with Elasticsearch.
    """
    def __init__(self, 
                 host=None, 
                 index_name=None):
        host = host 
        self.es = Elasticsearch(host)
        self.index_name = index_name

    def create_index(self):
        """
        Create the Elasticsearch index.
        """
        if self.es.indices.exists(index=self.index_name):
            self.es.indices.delete(index=self.index_name, ignore=[400, 404])
        self.es.indices.create(index=self.index_name)
        logger.info(f"Created Elasticsearch index: {self.index_name}")

    def save_transcription(self, doc):
        result = self.es.index(index=self.index_name, document=doc)
        logger.info(f"Saved transcription to Elasticsearch: {result['_id']}")
        return result

    def search_transcription(self, query):
        return self.es.search(index=self.index_name, query=query)

    def index_document(self, doc_id, document):
        """
        Index a document in Elasticsearch.
        """
        logger.info(f"Indexing document in Elasticsearch: {doc_id}")
        return self.es.index(index=self.index_name, id=doc_id, document=document)
    
    def update(self, index, id, body):
        logger.info(f"Updating document in Elasticsearch: {id}")
        return self.es.update(index=index, id=id, body=body)