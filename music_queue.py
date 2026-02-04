import time
from typing import Any
from threading import Event
from media_player import MediaPlayer

class Queue:
    """A first in, first out (FIFO) queue.

    Items are added to the back of the queue and removing items shifts the front pointer forward by 1, making every method O(1) time complexity.
    Supports enqueue, dequeue, peek, checking if the queue is empty and getting queue size.
    """
    def __init__(self):
        """Intialises the queue object.
        """
        self._queue = []
        self._front = 0

    def enqueue(self, item: Any):
        """Adds an item to the back of the queue.

        Args:
            item (Any): Any object to be added to the back of the queue.
        """
        self._queue.append(item)

    def dequeue(self) -> Any:
        """Removes an object at the front, average O(1) time complexity but occasionally cleans up the queue.

        Raises:
            IndexError: If the queue is empty, raise an ``IndexError``.

        Returns:
            Any: The object at the front of the queue.
        """
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        item = self._queue[self._front]
        self._front += 1

        # Cleanup the queue to not cause a memory leak
        if self._front > 50 and self._front > len(self._queue) // 2:
            self._queue = self._queue[self._front:]
            self._front = 0

        return item
    
    def peek(self) -> Any:
        """Peek the item at the front of the queue.

        Raises:
            IndexError: If the queue is empty, raise an ``IndexError``.

        Returns:
            Any: The object at the front of the queue.
        """
        if self.is_empty():
            raise IndexError("Peek from empty queue")
        return self._queue[self._front]
    
    def is_empty(self) -> bool:
        """Checks if there are items in the queue.

        Returns:
            bool: ``False`` if the queue is empty, ``True`` if the queue qcontains items.
        """
        return self._front == len(self._queue)
    
    def size(self) -> int:
        """Gets the size (length) of the queue.

        Returns:
            int: An int representing how many items are in the queue.
        """
        return len(self._queue) - self._front
    
class MusicQueue(Queue):
    """A first in, first out (FIFO) queue, handling songs queued up and playing them as each finishes.
    """
    def __init__(self, media_player: MediaPlayer, stop_event: Event):
        """Initialises the MusicQueue with a mediaplayer and a stop event.

        Args:
            media_player (MediaPlayer): The ``MediaPlayer`` used to play and control songs.
            stop_event (Event): Threading event to stop threads cleanly.
        """
        super().__init__()
        self._media_player = media_player
        self.__stop_event = stop_event

    def add_to_queue(self, song_title: str):
        """Adds a song by song title to the queue and informs the user when it will play.

        Args:
            song_title (str): The internal metadata title of the song.
        """
        if song_title == "":
            print("No song selected")
            return
        self.enqueue(song_title)
        print(f"Added {song_title} to queue, will play in {self.size()} song(s)")

    def play_next_song(self):
        """Plays the next song in the queue.
        """
        if not self.is_empty():
            self._media_player.play_song(self._media_player.song_title_to_song(self.dequeue()))

    def pprint(self):
        """Pretty prints the queue in a 1-base indexed list
        """
        for i, item in enumerate(self._queue[self._front:], start=1):
            print(f"{i}. {item}")

    def queue_loop(self):
        """Ran on a seperate thread and handles the music queue, playing the next song in the queue as each one finishes.
        """
        while True:
            if self.__stop_event.is_set():
                break

            if self._media_player.get_finished():
                self.play_next_song()
            time.sleep(0.1)