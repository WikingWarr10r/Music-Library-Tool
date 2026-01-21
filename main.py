from media_player import MediaPlayer
from playlist_manager import PlaylistManager
import threading

media_player = MediaPlayer("music/")

playlist_manager = PlaylistManager("playlists/")
playlist_manager.load()
playlist_manager.get_playlist("IAMMUSIC")

playlist_manager.play_song(media_player)

def playlist_loop():
    while True:
        playlist_manager.run_playlist(media_player)

playlist_thread = threading.Thread(
    target=playlist_loop,
    daemon=True
)

playlist_thread.start()

while True:
    action = input().strip().lower()
    if action == "pause":
        media_player.pause()
        print("Pausing song")
    if action == "unpause":
        media_player.unpause()
        print("Unpausing song")
    if action == "skip":
        media_player.stop()
        print("Skipping song")
    if action == "restart":
        media_player.restart()
        print("Restarting Song")
    