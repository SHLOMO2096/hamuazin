import base64
from app.log.logger import Logger

logger = Logger.get_logger()

class Decoder:
    def __init__(self, encoded_string: str):
        self.encoded_string = encoded_string

    def decode(self):
        decoded_string = base64.b64decode(self.encoded_string)
        decoded_string = decoded_string.decode('utf-8')
        list_words =  decoded_string.lower().split(',')
        logger.info(f"Decoded words: {list_words}")
        return list_words

# if __name__ == "__main__":
#     decoder = Decoder("R2Vub2NpZGUsV2FyIENyaW1lcyxBcGFydGhlaWQsTWFzc2FjcmUsTmFrYmEsRGlzcGxhY2VtZW50LEh1bWFuaXRhcmlhbiBDcmlzaXMsQmxvY2thZGUsT2NjdXBhdGlvbixSZWZ1Z2VlcyxJQ0MsQkRT")
#     decoder1 = Decoder("RnJlZWRvbSBGbG90aWxsYSxSZXNpc3RhbmNlLExpYmVyYXRpb24sRnJlZSBQYWxlc3RpbmUsR2F6YSxDZWFzZWZpcmUsUHJvdGVzdCxVTlJXQQ==")
#     hostile_list = decoder.decode()
#     not_hostile_list = decoder1.decode()
#     print(hostile_list)
#     print(not_hostile_list)




