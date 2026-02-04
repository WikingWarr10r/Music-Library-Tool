import mutagen
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer
import json
from pathlib import Path
import datetime
import time
from threading import Event
class MediaPlayer:
    """Handles media playing and controlling the media including playing, pausing, looping.
    """
    def __init__(self, music_folder: str, stop_event:Event):
        """Initialises the MediaPlayer with a music folder and a stop event.

        Args:
            music_folder (str): Path to the folder containing music files.
            stop_event (Event): Threading event to stop threads cleanly.
        """
        self._HISTORY = Path("play_history.json")
        self._MUSIC_FOLDER = music_folder

        self._current_song = ""
        self._length = 0

        self._looping_song = None

        self._sub_ms = 0

        self.__stop_event = stop_event

        mixer.init()

    def load_history(self) -> dict:
        """Loads the JSON play history file for editing stats

        Returns:
            dict: A dictionary containing the contents of the JSON play history file.
        """
        if not self._HISTORY.exists():
            return {"tracks": {}}
        with open(self._HISTORY, "r") as f:
            return json.load(f)

    def play_song(self, song: str):
        """Plays a song based on file name.

        Args:
            song (str): The filename of the song
        """
        if song == "" or song == None:
            return
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

        mixer.music.load(song)
        mixer.music.play()

    def pause(self):
        """Pauses current song.
        """
        mixer.music.pause()

    def unpause(self):
        """Unpauses current song.
        """
        mixer.music.unpause()

    def stop(self):
        """Stops current song.
        """
        mixer.music.stop()
        self._current_song = ""

    def restart(self):
        """Restarts current song.
        """
        self._sub_ms = mixer.music.get_pos()
        mixer.music.set_pos(0)

    def get_finished(self) -> bool:
        """Checks if the current song is finished.

        Returns:
            bool: A bool showing if the song is finished or not.
        """
        if mixer.music.get_pos() == -1:
            return True
        return False
    
    def get_time(self) -> str:
        """Generates a formatted string showing how long is left of the current song in the form 00:00/00:00.

        Returns:
            str: A string representing the time into the song.
        """
        if not self._current_song == None:
            return f"{time.strftime('%M:%S', time.gmtime((mixer.music.get_pos() - self._sub_ms) / 1000))}/{time.strftime('%M:%S', time.gmtime(self._length))}"
        else:
            return "No song playing"
        
    def song_details(self):
        """Pretty prints details about the song including the title, artist and time remaining.
        """
        metadata = mutagen.File(f"{self._MUSIC_FOLDER}/{self._current_song}", easy=True)
        print(f"{metadata.get('title')[0]} by {metadata.get('artist')[0]} - {self.get_time()}")
        
    def start_looping(self):
        """Enables a flag for the looping thread to handle song looping.
        """
        self._looping_song = self._current_song
    
    def stop_looping(self):
        """Disables a flag for the looping thread to stop looping the current song.
        """
        self._looping_song = None

    def looping_loop(self):
        """Ran on a seperate thread and handles song looping by restarting the song whenever it finishes.
        """
        while True:
            if self.__stop_event.is_set():
                break
            if not self._looping_song == None:
                if self.get_finished():
                    self._current_song = self._looping_song
                    self.play_song(self._current_song)
            time.sleep(0.1)

    def set_volume(self, volume: float):
        """Sets the volume of a song to a certain value.

        Args:
            volume (float): A normalised float (0-1) which sets the volume of the music playing.
        """
        mixer.music.set_volume(volume)

    def preview_song_titles(self):
        """Prints all the songs in the music folder using their internal metadata names.
        """
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

    def song_title_to_song(self, title: str) -> str|None:
        """Converts the internal metadata song title to the filename or None.

        Args:
            title (str): This is the internal metadata song title.

        Returns:
            str|None: The filename of the song or None.
        """
        for song in os.listdir(self._MUSIC_FOLDER):
            song_metadata = mutagen.File(f"{self._MUSIC_FOLDER}/{song}", easy=True)
            if song_metadata:
                if song_metadata.get("title")[0] == title:
                    return song
        return None
    
    def song_title_to_metadata(self, title: str) -> mutagen.File|None:
        """Converts the internal metadata title to the full metadata of the song or None."

        Args:
            title (str): This is the internal metadata song title.

        Returns:
            mutagen.File|None: A mutagen file, similar to a dict containing the metadata of the song or None.
        """
        for song in os.listdir(self._MUSIC_FOLDER):
            song_metadata = mutagen.File(f"{self._MUSIC_FOLDER}/{song}", easy=True)
            if song_metadata:
                if song_metadata.get("title")[0] == title:
                    return song_metadata
        return None