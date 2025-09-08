import os

NAME = os.getenv("LOG_NAME", "muazin_loger")
ES_HOST = os.getenv("ES_HOST", "http://localhost:9200")
ES_INDEX = os.getenv("ES_INDEX", "logs")
