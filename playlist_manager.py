import csv
import time
from threading import Event
from media_player import MediaPlayer

class PlaylistManager:
    """Handles playlists, allowing playlist loading, creation, getting playlists, and listening to the playlist using a ``MediaPlayer``.
    """
    def __init__(self, playlist_folder: str, media_player: MediaPlayer, stop_event: Event):
        """Initialises the PlaylistManager with a playlist folder, media player and a stop event for threading.

        Args:
            playlist_folder (str): The file location of the playlists.
            media_player (MediaPlayer): The ``MediaPlayer`` used to play and control songs.
            stop_event (Event): Threading event to stop threads cleanly.
        """
        self._PLAYLIST_FOLDER = playlist_folder
        self._playlists = {}

        self._current_playlist = ""
        self._song_index = 0
        self._media_player = media_player

        self.__stop_event = stop_event

    def load(self):
        """Loads the playlists from the CSV file into memory for reading/editing.
        """
        with open(f"{self._PLAYLIST_FOLDER}/playlists.csv", newline="") as f:
            for row in csv.reader(f):
                if not row:
                    continue
                name = row[0]
                songs = row[1:]
                self._playlists[name] = songs
    
    def write_playlists(self):
        """Writes any local edits into the playlists CSV file for storage. 

        Call when finished editing.
        """
        with open(f"{self._PLAYLIST_FOLDER}/playlists.csv", "w", newline="") as f:
            writer = csv.writer(f)
            for name, songs in self._playlists.items():
                writer.writerow([name, *songs])
    
    def create_playlist(self):
        """Creates a playlist of any length and stores it for playing later.
        """
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

    def get_playlist(self, name: str|int):
        """Sets the internal playlist of the ``PlaylistManager`` to a playlist name or the index of the playlist.

        Args:
            name (str|int): The name of the playlist.
        """
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

    def get_song_in_playlist(self) -> str:
        """Returns the song title of the current playlist and the current song index within that playlist.

        Returns:
            str: The song title that is currently selected.
        """
        return self._playlists[self._current_playlist][self._song_index]
    
    def get_playlists(self) -> dict:
        """Gets all playlists and returns them as a dictionary with the key-value pair being playlist title and songs.

        Returns:
            dict: A dictionary containing all the playlists
        """
        return self._playlists
    
    def get_tracklist(self) -> list:
        """Gets all songs after the current song being played for display.

        Returns:
            list: A list containing all the songs after the currently played song.
        """
        return self._playlists[self._current_playlist][self._song_index:]

    def next_song(self):
        """Increments the song index of the playlist, looping back to the start after completing it.
        """
        playlist = self._playlists[self._current_playlist]
        self._song_index = (self._song_index + 1) % len(playlist)

    def play_song(self):
        """Uses the ``MediaPlayer`` to play the current song in the playlist.
        """
        self._media_player.play_song(self._media_player.song_title_to_song(self.get_song_in_playlist()))

    def run_playlist(self):
        """Continues the playlist after each song finishes.
        """
        if self._media_player.get_finished():
            self.next_song()
            self.play_song()

    def playlist_loop(self):
        """Ran on a seperate thread and handles the playlist, continuing to the next song after each finishes.
        """
        while True:
            if self.__stop_event.is_set():
                break
            self.run_playlist()
            time.sleep(0.1)