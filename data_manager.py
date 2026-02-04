import json
from datetime import datetime
from helpers import best_match

class SongData:
    """Holds the data from the JSON as an object in memory for later retrieval and sorting.
    """
    def __init__(self, title: str, track_data: dict):
        self.title = title
        self.play_count = track_data["play_count"]
        self.last_played = datetime.fromisoformat(track_data["last_played"])
    
    def __repr__(self):
        return f"{self.title:<25} | {self.play_count:^6} | {self.last_played.strftime('%d %b %Y, %H:%M')}"

class DataManager:
    def __init__(self):
        """Manages a list of ``SongData`` objects for displaying and sorting. 
        """
        self._songs = []

    def load(self):
        """Loads the ``play_history.json`` file into a list of ``SongData`` objects.
        """
        self._songs = []
        with open("play_history.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            for track_name, track_data in data["tracks"].items():
                self._songs.append(SongData(track_name, track_data))
    
    def sort_data(self):
        """Sorts the loaded data based on when it was last played or how many times it's been played.
        """
        sort_by = input("Do you want to sort by last played or play count: ")
        if best_match(sort_by.lower().strip(), ["last played", "play count"])[0] == "last played":
            self._songs.sort(key=lambda s: s.last_played, reverse=True)
        else:
            self._songs.sort(key=lambda s: s.play_count, reverse=True)
    
    def display_data(self):
        """Displays the data in a table.
        """
        print("Index | Title                     | Plays  | Last Played")
        for index, song in enumerate(self._songs, start=1):
            print(f"{index:<5} | {song}")