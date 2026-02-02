class MetadataEditor:
    @staticmethod
    def rename_song(metadata):
        metadata["title"] = input("Enter New Title: ")

    @staticmethod
    def set_artist(metadata):
        if "artist" in metadata:
            metadata["artist"] = input("Enter New Artist Name: ")
        elif "albumartist" in metadata:
            metadata["albumartist"] = input("Enter New Artist Name: ")
        else:
            print("Unknown Format")

    @staticmethod
    def set_album(metadata):
        metadata["album"] = input("Enter New Album Title: ")
