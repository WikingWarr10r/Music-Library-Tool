import json
from datetime import datetime

class SongData:
    def __init__(self, title, track_data):
        self.title = title
        self.play_count = track_data["play_count"]
        self.last_played = datetime.fromisoformat(track_data["last_played"])
    
    def __repr__(self):
        return f"{self.title:<25} | {self.play_count:^6} | {self.last_played.strftime('%d %b %Y, %H:%M')}"

songs = []

with open("play_history.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    for track_name, track_data in data["tracks"].items():
        songs.append(SongData(track_name, track_data))

songs.sort(key=lambda s: s.last_played, reverse=True)

print("Index | Title                     | Plays  | Last Played")
for index, song in enumerate(songs, start=1):
    print(f"{index:<5} | {song}")