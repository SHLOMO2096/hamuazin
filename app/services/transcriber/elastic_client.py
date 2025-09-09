import os
from elasticsearch import Elasticsearch
import config

class ElasticSearchClient:
    def __init__(self, 
                 host=None, 
                 index_name=None):
        host = host 
        self.es = Elasticsearch(host)
        self.index_name = index_name

    def create_index(self):
        if self.es.indices.exists(index=self.index_name):
            self.es.indices.delete(index=self.index_name, ignore=[400, 404])
        self.es.indices.create(index=self.index_name)

    def save_transcription(self, doc):
        return self.es.index(index=self.index_name, document=doc)

    def search_transcription(self, query):
        return self.es.search(index=self.index_name, query=query)

    def index_document(self, doc_id, document):
        return self.es.index(index=self.index_name, id=doc_id, document=document)