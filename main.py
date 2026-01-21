from media_player import MediaPlayer
from playlist_manager import PlaylistManager
from helpers import best_match
import threading

COMMANDS = ["pause", "unpause", "skip", "restart", "list", "time", "help"]

media_player = MediaPlayer("music/")

playlist_manager = PlaylistManager("playlists/")
playlist_manager.load()

def playlist_loop():
    while True:
        playlist_manager.run_playlist(media_player)

choice = input("\nCreate playlist\nPlay playlist\n")

if "create" in choice.lower():
    playlist_manager.create_playlist(media_player)
elif "play" in choice.lower():
    for index, playlist in enumerate(playlist_manager.get_playlists()):
        print(f"{index+1}. {playlist}")
    playlist_manager.get_playlist(input("Enter Playlist to play: "))

    playlist_manager.play_song(media_player)

    playlist_thread = threading.Thread(target=playlist_loop,daemon=True)

    playlist_thread.start()

    while True:
        inp = input().strip().lower()

        best = best_match(inp, COMMANDS)

        if best[1] < 4:
            action = best[0]
        else:
            action = None
            print(f"Unknown command, did you mean {best[0]}")

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
        if action == "list":
            for index, song in enumerate(playlist_manager.get_tracklist()):
                print(f"{index+1}. {song}")
        if action == "time":
            print(media_player.get_time())
        if action == "help":
            print("Available Actions:")
            for command in COMMANDS:
                print(command)