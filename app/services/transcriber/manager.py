import gridfs
import config_transcriber
from mongo_client import MongoHandler
from elastic_client import ElasticSearchClient
from faster_whisper import WhisperModel
from app.log.logger import Logger

logger = Logger.get_logger()

class TranscriberManager:
    """
    Manager for handling audio transcription.
    """
    def __init__(self, mongo_uri, mongo_db, mongo_collection, es_host):
        self.mongo_handler = MongoHandler(mongo_uri, mongo_db, mongo_collection)
        self.es_client = ElasticSearchClient(es_host)
        self.whisper_model = WhisperModel("base") 
        self.model = WhisperModel("base", device="cpu", compute_type="int8")
        self.fs = gridfs.GridFS(self.mongo_handler.db)

    
    def transcribe(self, audio_path):
        """
        Transcribe audio file using Whisper model.
        """
        segments, info = self.model.transcribe(audio_path, beam_size=5, task="translate")

        logger.info(f"Detected language '{info.language}' with probability {info.language_probability}")

        full_text = ""
        for segment in segments:
            full_text += segment.text

        return full_text

    def process_one(self, doc):
        """
        Process a single document.
        """
        uuid = str(doc["uuid"])
        mongo_id = doc["file_id"]  

        audio_file = self.fs.get(mongo_id).read()

        with open("temp_audio.wav", "wb") as f:
            f.write(audio_file)

        transcript = self.transcribe("temp_audio.wav")
        
        # update in ElasticSearch
        self.es_client.update(
            index="audio_index",
            id=uuid,
            body={"doc": {"transcript": transcript}}
        )
        # update in MongoDB (flag that transcription exists)
        self.mongo_handler.update_document(  
            {"_id": doc["_id"]},
            {"$set": {"transcribed": True, "transcript": transcript}}
        )

        logger.info(f"Transcribed and updated UUID={uuid}")


    def main(self):
        """
        Main processing loop.
        """
        docs = self.mongo_handler.find_documents({"transcribed": {"$ne": True}})

        for doc in docs:
            try:
                self.process_one(doc)
            except Exception as e:
                logger.error(f"Error with doc {doc['_id']}: {e}")



if __name__ == "__main__":
    transcriber = TranscriberManager(
        config_transcriber.MONGO_URI,
        config_transcriber.MONGO_DB,
        config_transcriber.MONGO_COLLECTION,
        config_transcriber.ES_HOST)
    transcriber.main()

