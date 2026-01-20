import mutagen
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer
import json
from pathlib import Path
import datetime

class MediaPlayer:
    def __init__(self, music_folder):
        self.HISTORY = Path("play_history.json")
        self.MUSIC_FOLDER = music_folder

        self.current_song = ""

    def load_history(self):
        if not self.HISTORY.exists():
            return {"tracks": {}}
        with open(self.HISTORY, "r") as f:
            return json.load(f)

    def play_song(self, song: str):
        self.current_song = song
        data = self.load_history()

        song = f"{self.MUSIC_FOLDER}/{song}"
        try:
            song_metadata = mutagen.File(song, easy=True)
        except Exception as e:
            song_metadata = mutagen.File(self.song_title_to_song(song), easy=True)
            print("Exception caught, forgot to convert song title to song")
        if song_metadata:
            title = song_metadata.get("title", "Unknown Title")[0]
            print(f"Playing: {title}")
        else:
            print(f"Couldn't read metadata for {song}")
        

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

    def pause(self):
        mixer.music.pause()

    def unpause(self):
        mixer.music.unpause()

    def stop(self):
        mixer.music.stop()
        self.current_song = ""

    def restart(self):
        song = self.current_song
        self.stop()
        self.play_song(song)

    def get_finished(self) -> bool:
        if mixer.music.get_pos() == -1:
            return True
        return False

    def preview_song_titles(self):
        songs = os.listdir(self.MUSIC_FOLDER)
        for sng in songs:
            song = f"{self.MUSIC_FOLDER}/{sng}"
            song_metadata = mutagen.File(song, easy=True)
            if song_metadata:
                title = song_metadata.get("title", "Unknown Title")[0]
                artist = song_metadata.get("artist", "Unkown Artist")[0]
                print(f"{title} by {artist}")
            else:
                print(f"Couldn't read metadata for {song}")

    def song_title_to_song(self, title):
        for song in os.listdir(self.MUSIC_FOLDER):
            song_metadata = mutagen.File(f"{self.MUSIC_FOLDER}/{song}", easy=True)
            if song_metadata:
                if song_metadata.get("title")[0] == title:
                    return song
        return None
