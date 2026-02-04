import csv
import time

class PlaylistManager:
    def __init__(self, playlist_folder, media_player, stop_event):
        self._PLAYLIST_FOLDER = playlist_folder
        self._playlists = {}

        self._current_playlist = ""
        self._song_index = 0
        self._media_player = media_player

        self.__stop_event = stop_event

    def load(self):
        with open(f"{self._PLAYLIST_FOLDER}/playlists.csv", newline="") as f:
            for row in csv.reader(f):
                if not row:
                    continue
                name = row[0]
                songs = row[1:]
                self._playlists[name] = songs
    
    def write_playlists(self):
        with open(f"{self._PLAYLIST_FOLDER}/playlists.csv", "w", newline="") as f:
            writer = csv.writer(f)
            for name, songs in self._playlists.items():
                writer.writerow([name, *songs])
    
    def create_playlist(self):
        playlist_name = input("Enter playlist name: ")

        if playlist_name in self._playlists:
            print("Playlist already exists")
            return

        self._media_player.preview_song_titles()

        songs = []
        while True:
            song = input("Enter song title: ")
            if song == "":
                break

            if self._media_player.song_title_to_song(song) is not None:
                songs.append(song)
            else:
                print(f"The song {song} was not found")

        self._playlists[playlist_name] = songs
        self.write_playlists()

    def get_playlist(self, name):
        if name.isdigit():
            index = int(name) - 1
            playlist_names = list(self._playlists.keys())

            if 0 <= index < len(playlist_names):
                self._current_playlist = playlist_names[index]
            else:
                print("Invalid playlist number")
                return
        else:
            if name not in self._playlists:
                print("Playlist not found")
                return
            self._current_playlist = name

        self._song_index = 0

    def get_song_in_playlist(self):
        return self._playlists[self._current_playlist][self._song_index]
    
    def get_playlists(self):
        return self._playlists
    
    def get_tracklist(self):
        return self._playlists[self._current_playlist][self._song_index:]

    def next_song(self):
        playlist = self._playlists[self._current_playlist]
        self._song_index = (self._song_index + 1) % len(playlist)

    def play_song(self):
        self._media_player.play_song(self._media_player.song_title_to_song(self.get_song_in_playlist()))

    def run_playlist(self):
        if self._media_player.get_finished():
            self.next_song()
            self.play_song()

    def playlist_loop(self):
        while True:
            if self.__stop_event.is_set():
                break
            self.run_playlist()
            time.sleep(0.1)