import csv

class PlaylistManager:
    def __init__(self, playlist_folder):
        self.playlist_folder = playlist_folder
        self.playlists = {}

        self.current_playlist = ""
        self.song_index = 0

    def load(self):
        with open(f"{self.playlist_folder}/playlists.csv", newline="") as f:
            for row in csv.reader(f):
                if not row:
                    continue
                name = row[0]
                songs = row[1:]
                self.playlists[name] = songs
    
    def write_playlists(self):
        with open(f"{self.playlist_folder}/playlists.csv", "w", newline="") as f:
            writer = csv.writer(f)
            for name, songs in self.playlists.items():
                writer.writerow([name, *songs])
    
    def create_playlist(self, media_player):
        playlist_name = input("Enter playlist name: ")

        if playlist_name in self.playlists:
            print("Playlist already exists")
            return

        media_player.preview_song_titles()

        songs = []
        while True:
            song = input("Enter song title: ")
            if song == "":
                break

            if media_player.song_title_to_song(song) is not None:
                songs.append(song)
            else:
                print(f"The song {song} was not found")

        self.playlists[playlist_name] = songs
        self.write_playlists()

    def get_playlist(self, name):
        self.current_playlist = name
        self.song_index = 0

    def get_song_in_playlist(self):
        return self.playlists[self.current_playlist][self.song_index]

    def next_song(self):
        playlist = self.playlists[self.current_playlist]
        self.song_index = (self.song_index + 1) % len(playlist)

    def play_song(self, media_player):
        media_player.play_song(media_player.song_title_to_song(self.get_song_in_playlist()))

    def run_playlist(self, media_player):
        if media_player.get_finished():
            self.next_song()
            self.play_song()