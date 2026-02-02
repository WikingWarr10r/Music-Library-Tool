import mutagen
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer
import json
from pathlib import Path
import datetime
import time

class MediaPlayer:
    def __init__(self, music_folder):
        self._HISTORY = Path("play_history.json")
        self._MUSIC_FOLDER = music_folder

        self._current_song = ""
        self._length = 0

        self._looping_song = None

        self._sub_ms = 0

    def load_history(self):
        if not self._HISTORY.exists():
            return {"tracks": {}}
        with open(self._HISTORY, "r") as f:
            return json.load(f)

    def play_song(self, song: str):
        self._sub_ms = 0
        self._current_song = song
        data = self.load_history()

        song = f"{self._MUSIC_FOLDER}/{song}"
        try:
            song_metadata = mutagen.File(song, easy=True)
        except Exception as e:
            song_metadata = mutagen.File(self.song_title_to_song(song), easy=True)
            print("Exception caught, forgot to convert song title to song")
        if song_metadata:
            title = song_metadata.get("title", "Unknown Title")[0]
            self._length = song_metadata.info.length
            print(f"Playing: {title}")
        else:
            print(f"Couldn't read metadata for {song}")
        

        track = data["tracks"].setdefault(title, {
            "play_count": 0,
            "last_played": None,
        })

        track["play_count"] += 1
        track["last_played"] = datetime.datetime.now().isoformat()

        with open(self._HISTORY, "w") as f:
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
        self._current_song = ""

    def restart(self):
        self._sub_ms = mixer.music.get_pos()
        mixer.music.set_pos(0)

    def get_finished(self) -> bool:
        if mixer.music.get_pos() == -1:
            return True
        return False
    
    def get_time(self):
        if not self._current_song == None:
            return f"{time.strftime('%M:%S', time.gmtime((mixer.music.get_pos() - self._sub_ms) / 1000))}/{time.strftime('%M:%S', time.gmtime(self._length))}"
        else:
            return "No song playing"
        
    def song_details(self):
        metadata = mutagen.File(f"{self._MUSIC_FOLDER}/{self._current_song}", easy=True)
        print(f"{metadata.get('title')[0]} by {metadata.get('artist')[0]} - {self.get_time()}")
        
    def start_looping(self):
        self._looping_song = self._current_song
    
    def stop_looping(self):
        self._looping_song = None

    def looping_loop(self):
        while True:
            if not self._looping_song == None:
                if self.get_finished():
                    self._current_song = self._looping_song
                    self.play_song(self._current_song)
            time.sleep(0.1)

    def set_volume(self, volume):
        mixer.music.set_volume(volume)

    def preview_song_titles(self):
        songs = os.listdir(self._MUSIC_FOLDER)
        for sng in songs:
            song = f"{self._MUSIC_FOLDER}/{sng}"
            song_metadata = mutagen.File(song, easy=True)
            if song_metadata:
                title = song_metadata.get("title", "Unknown Title")[0]
                artist = song_metadata.get("artist", "Unkown Artist")[0]
                print(f"{title} by {artist}")
            else:
                print(f"Couldn't read metadata for {song}")

    def song_title_to_song(self, title):
        for song in os.listdir(self._MUSIC_FOLDER):
            song_metadata = mutagen.File(f"{self._MUSIC_FOLDER}/{song}", easy=True)
            if song_metadata:
                if song_metadata.get("title")[0] == title:
                    return song
        return None
    
    def song_title_to_metadata(self, title) -> dict:
        for song in os.listdir(self._MUSIC_FOLDER):
            song_metadata = mutagen.File(f"{self._MUSIC_FOLDER}/{song}", easy=True)
            if song_metadata:
                if song_metadata.get("title")[0] == title:
                    return song_metadata
        return None