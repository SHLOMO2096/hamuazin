from tinytag import TinyTag

import json

class MetadataCreator:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_audio_metadata(self) -> dict:
        """

        """
        tag = TinyTag.get(self.file_path)
        return {
            "duration": tag.duration,
            "sample_rate": tag.samplerate,
            "bitrate": tag.bitrate,
            "channels": tag.channels,
            "filesize": tag.filesize,
            "artist": tag.artist,
            "album": tag.album,
            "title": tag.title
        }

if __name__ == "__main__":
    creator = MetadataCreator("C:\\Users\\shlomo\\Downloads\\podcasts\\download (1).wav")
    metadata = creator.get_audio_metadata()
    print(metadata)
