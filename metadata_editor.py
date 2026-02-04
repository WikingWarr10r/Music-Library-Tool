import mutagen
class MetadataEditor:
    """Handles the editing of metadata with static methods.
    This system can handle any filetype that ``mutagen`` can handle.
    """
    @staticmethod
    def rename_song(metadata: mutagen.File):
        """Renames a song from the metadata of that song.

        Args:
            metadata (mutagen.File): The mutagen metadata file object to edit.
        """
        metadata["title"] = input("Enter New Title: ")

    @staticmethod
    def set_artist(metadata: mutagen.File):
        """Changes the artist of a song from the metadata of that song.

        Args:
            metadata (mutagen.File): The mutagen metadata file object to edit.
        """
        if "artist" in metadata:
            metadata["artist"] = input("Enter New Artist Name: ")
        elif "albumartist" in metadata:
            metadata["albumartist"] = input("Enter New Artist Name: ")
        else:
            print("Unknown Format")

    @staticmethod
    def set_album(metadata: mutagen.File):
        """Sets the album of a song from the metadata of that song.

        Args:
            metadata (mutagen.File): The mutagen metadata file object to edit.
        """
        metadata["album"] = input("Enter New Album Title: ")
