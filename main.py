from media_player import MediaPlayer
from playlist_manager import PlaylistManager
from metadata_editor import MetadataEditor
from helpers import best_match
import threading

COMMANDS = ["pause", "unpause", "skip", "restart", "list", "time", "stop", "loop", "unloop", "play", "volume", "help"]
EDIT_COMMANDS = ["title", "artist", "album", "stop", "new", "help", "debug"]

media_player = MediaPlayer("music/")

playlist_manager = PlaylistManager("playlists/", media_player)
playlist_manager.load()

metadata_editor = MetadataEditor()

choice = input("\nCreate playlist\nEdit metadata\nPlay songs\n")

if "create" in choice.lower():
    playlist_manager.create_playlist()
if "edit" in choice.lower():
    media_player.preview_song_titles()
    metadata = media_player.song_title_to_metadata(input('Enter song to edit: '))
    while True:
        try:
            inp = input().strip().lower()
            best = best_match(inp, EDIT_COMMANDS)

            if best[1] < 4:
                action = best[0]
            else:
                action = None
                print(f"Unknown command, did you mean {best[0]}")

            if action == "new":
                media_player.preview_song_titles()
                metadata = media_player.song_title_to_metadata(input('Enter song to edit: '))
            if action == "title":
                metadata_editor.rename_song(metadata)
            if action == "artist":
                metadata_editor.set_artist(metadata)
            if action == "album":
                metadata_editor.set_album(metadata)
            if action == "debug":
                print(metadata)
            if action == "stop":
                break
            if action == "help":
                print("Available Actions:")
                for command in EDIT_COMMANDS:
                    print(command)
            metadata.save()
        except Exception as e:
            print(f"An error occured: {e}")

elif "play" in choice.lower():
    if "y" in input("Do you want to play a playlist: ").strip().lower():
        for index, playlist in enumerate(playlist_manager.get_playlists()):
            print(f"{index+1}. {playlist}")
        playlist_manager.get_playlist(input("Enter Playlist to play: "))
        playlist_manager.play_song()

        playlist_thread = threading.Thread(target=playlist_manager.playlist_loop,daemon=True)
        playlist_thread.start()
    else:
        media_player.preview_song_titles()
        current_song = media_player.song_title_to_song(input('Enter song to play: '))
        media_player.play_song(current_song)

        looping_thread = threading.Thread(target=media_player.looping_loop,daemon=True)
        looping_thread.start()

    while True:
        try:
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
            if action == "stop":
                print("Stopping")
                break
            if action == "loop":
                media_player.start_looping()
                print("Looping current song")
            if action == "unloop":
                media_player.stop_looping()
                print("Unlooping current song")
            if action == "play":
                media_player.preview_song_titles()
                current_song = media_player.song_title_to_song(input('Enter song to play: '))
                media_player.play_song(current_song)
            if action == "volume":
                media_player.set_volume(float(input("Enter Volume: "))/100)
            if action == "help":
                print("Available Actions:")
                for command in COMMANDS:
                    print(command)
        except Exception as e:
            print(f"An error occured: {e}")