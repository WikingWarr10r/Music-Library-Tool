from media_player import MediaPlayer
from playlist_manager import PlaylistManager
from metadata_editor import MetadataEditor
from music_queue import MusicQueue
from data_manager import DataManager
from helpers import best_match
import threading

# List of potential commands for use with Levenshtein Distance Function
COMMANDS = ["pause", "unpause", "skip", "restart", "list", "time", "stop", "loop", "unloop", "play", "volume", "queue", "details", "help"]
EDIT_COMMANDS = ["title", "artist", "album", "stop", "new", "help", "debug"]
VIEW_COMMANDS = ["load", "sort", "view", "stop", "help"]

stop_event = threading.Event()

media_player = MediaPlayer("music/", stop_event)

playlist_manager = PlaylistManager("playlists/", media_player, stop_event)
playlist_manager.load()

queue = MusicQueue(media_player, stop_event)

data_manager = DataManager()

choice = input("\nCreate playlist\nEdit metadata\nPlay songs\nView Song Data\n")

# Create Playlists
if "create" in choice.lower():
    playlist_manager.create_playlist()

# Edit Metadata
elif "edit" in choice.lower():
    media_player.preview_song_titles()
    metadata = media_player.song_title_to_metadata(input("Enter song to edit: "))
    while True:
        try:
            # Runs commands, using Levenshtein distance to fix errors in spelling or prompt the user if the word was too difficult
            inp = input().strip().lower()
            best = best_match(inp, EDIT_COMMANDS)

            if best[1] < 4:
                action = best[0]
            else:
                action = None
                print(f"Unknown command, did you mean {best[0]}")

            if action == "new":
                media_player.preview_song_titles()
                metadata = media_player.song_title_to_metadata(input("Enter song to edit: "))
            if action == "title":
                MetadataEditor.rename_song(metadata)
            if action == "artist":
                MetadataEditor.set_artist(metadata)
            if action == "album":
                MetadataEditor.set_album(metadata)
            if action == "debug":
                print(metadata)
            if action == "stop":
                print("Stopping")
                stop_event.set()
                break
            if action == "help":
                print("Available Actions:")
                for command in EDIT_COMMANDS:
                    print(command)
            metadata.save()
        except Exception as e:
            print(f"An error occured: {e}")

# View song data
elif "view" in choice.lower():
        action = ""
        while True:
            # Runs commands, using Levenshtein distance to fix errors in spelling or prompt the user if the word was too difficult
            inp = input().strip().lower()
            best = best_match(inp, VIEW_COMMANDS)

            if best[1] < 4:
                action = best[0]
            else:
                action = None
                print(f"Unknown command, did you mean {best[0]}")

            if action == "load":
                data_manager.load()
                print("Loaded song data")
            if action == "sort":
                data_manager.sort_data()
                print("Sorted data")
            if action == "view":
                data_manager.display_data()
            if action == "stop":
                print("Stopping")
                stop_event.set()
                break
            if action == "help":
                print("Available Actions:")
                for command in VIEW_COMMANDS:
                    print(command)

# Play song/playlist
elif "play" in choice.lower():
    # Play a playlist and start the playlist thread
    if "y" in input("Do you want to play a playlist: ").strip().lower():
        for index, playlist in enumerate(playlist_manager.get_playlists()):
            print(f"{index+1}. {playlist}")
        playlist_manager.get_playlist(input("Enter Playlist to play: "))
        playlist_manager.play_song()

        playlist_thread = threading.Thread(target=playlist_manager.playlist_loop,daemon=True)
        playlist_thread.start()
    # Play a song from the music folder and start he looping and queue threads
    else:
        media_player.preview_song_titles()
        current_song = media_player.song_title_to_song(input("Enter song to play: "))
        media_player.play_song(current_song)

        looping_thread = threading.Thread(target=media_player.looping_loop,daemon=True)
        looping_thread.start()

        queue_thread = threading.Thread(target=queue.queue_loop,daemon=True)
        queue_thread.start()

    while True:
        try:
            # Runs commands, using Levenshtein distance to fix errors in spelling or prompt the user if the word was too difficult
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
                # Shows the next songs in the queue or the playlist depnding on which mode we're running
                if queue.is_empty():
                    for index, song in enumerate(playlist_manager.get_tracklist()):
                        print(f"{index+1}. {song}")
                else:
                    queue.pprint()
            if action == "time":
                print(media_player.get_time())
            if action == "stop":
                print("Stopping")
                stop_event.set()
                break
            if action == "loop":
                if queue.is_empty():
                    media_player.start_looping()
                    print("Looping current song")
                else:
                    print("Cannot loop while queue is full")
            if action == "unloop":
                media_player.stop_looping()
                print("Unlooping current song")
            if action == "play":
                media_player.preview_song_titles()
                current_song = media_player.song_title_to_song(input("Enter song to play: "))
                media_player.play_song(current_song)
            if action == "volume":
                media_player.set_volume(float(input("Enter Volume: "))/100)
            if action == "queue":
                media_player.preview_song_titles()
                queue.add_to_queue(input("Enter Song to queue: "))
            if action == "details":
                media_player.song_details()
            if action == "help":
                print("Available Actions:")
                for command in COMMANDS:
                    print(command)
        
        # Exception Handling
        except Exception as e:
            print(f"An error occured: {e}")