from media_player import MediaPlayer
class MetadataEditor:
    def __init__(self):
        self.song = None

    def rename_song(self, metadata):
        metadata["title"] = input("Enter New Title: ")

    def set_artist(self, metadata):
        if "artist" in metadata:
            metadata["artist"] = input("Enter New Artist Name: ")
        elif "albumartist" in metadata:
            metadata["albumartist"] = input("Enter New Artist Name: ")
        else:
            print("Unknown Format")

    def set_album(self, metadata):
        metadata["album"] = input("Enter New Album Title: ")
