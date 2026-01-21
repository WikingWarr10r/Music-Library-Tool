import threading
import time
from media_player import MediaPlayer
from playlist_manager import PlaylistManager

media_player = MediaPlayer("music/")

playlist_manager = PlaylistManager("playlists/")
playlist_manager.load()
playlist_manager.get_playlist("IAMMUSIC")

playlist_manager.play_song(media_player)

running = True

def playlist_loop():
    while running:
        playlist_manager.run_playlist(media_player)
        time.sleep(0.1)

playlist_thread = threading.Thread(target=playlist_loop, daemon=True)
playlist_thread.start()

while True:
    action = input("Do you want to pause, unpause, stop or restart: ").strip().lower()
    if action == "pause":
        media_player.pause()
        print("Pausing song")
    if action == "unpause":
        media_player.unpause()
        print("Unpausing song")
    if action == "stop":
        media_player.stop()
        print("Stopping song")
        media_player.preview_song_titles()
        current_song = media_player.song_title_to_song(input('Enter song to play: '))
        media_player.play_song(current_song)
    if action == "restart":
        media_player.restart()
        print("Restarting Song")
