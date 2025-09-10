import os


MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "podcasts")
MONGO_DB = os.getenv("MONGO_DB", "podcasts_db")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
ES_HOST = os.getenv("ELASTIC_URI", "http://localhost:9200")
ES_INDEX = os.getenv("ES_INDEX", "podcasts")
HOSTILE_WORDS_CODED = ("R2Vub2NpZGUsV2FyIENyaW1lcyxBcGFydGhlaWQsTWFzc2FjcmUsTmFrYmEsRGlzcGxhY2VtZW50LEh1bWFuaXRhcmlhbiBDcmlzaXMsQmxvY2thZGUsT2NjdXBhdGlvbixSZWZ1Z2VlcyxJQ0MsQkRT")
NON_HOSTILE_WORDS_CODED = ("RnJlZWRvbSBGbG90aWxsYSxSZXNpc3RhbmNlLExpYmVyYXRpb24sRnJlZSBQYWxlc3RpbmUsR2F6YSxDZWFzZWZpcmUsUHJvdGVzdCxVTlJXQQ==")