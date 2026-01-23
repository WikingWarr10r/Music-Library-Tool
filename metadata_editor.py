import mutagen
from media_player import MediaPlayer
class MetadataEditor:
    def __init__(self, media_player: MediaPlayer):
        self.song = None
        self.media_player = media_player