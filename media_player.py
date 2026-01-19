import mutagen
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer
import json
from pathlib import Path
import datetime

class MediaPlayer:
    def __init__(self):
        self.HISTORY = Path("play_history.json")

    def load_history(self):
        if not self.HISTORY.exists():
            return {"tracks": {}}
        with open(self.HISTORY, "r") as f:
            return json.load(f)

    def play_song(self, song: str):
        data = self.load_history()

        song_metadata = mutagen.File(song, easy=True)
        if song_metadata:
            title = song_metadata.get("title", "Unknown Title")
            if isinstance(title, list):
                title = title[0]
            print(f"Playing: {title}")
        else:
            print(f"Could not read metadata for {song}")
        

        track = data["tracks"].setdefault(title, {
            "play_count": 0,
            "last_played": None,
        })

        track["play_count"] += 1
        track["last_played"] = datetime.datetime.now().isoformat()

        with open(self.HISTORY, "w") as f:
            json.dump(data, f, indent=2)

        mixer.init()
        mixer.music.load(song)
        mixer.music.play()