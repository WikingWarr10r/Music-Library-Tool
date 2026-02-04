import time

class Queue:
    def __init__(self):
        self._queue = []
        self._front = 0

    def enqueue(self, item):
        self._queue.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        item = self._queue[self._front]
        self._front += 1
        return item
    
    def peek(self):
        if self.is_empty():
            raise IndexError("Peek from empty queue")
        return self._queue[self._front]
    
    def is_empty(self):
        return self._front == len(self._queue)
    
    def size(self):
        return len(self._queue) - self._front
    
class MusicQueue(Queue):
    def __init__(self, media_player, stop_event):
        super().__init__()
        self._media_player = media_player
        self.__stop_event = stop_event

    def add_to_queue(self, song_title):
        if song_title == "":
            print("No song selected")
            return
        self.enqueue(song_title)
        print(f"Added {song_title} to queue, will play in {self.size()} song(s)")

    def play_next_song(self):
        if not self.is_empty():
            self._media_player.play_song(self._media_player.song_title_to_song(self.dequeue()))

    def pprint(self):
        for i, item in enumerate(self._queue[self._front:], start=1):
            print(f"{i}. {item}")

    def queue_loop(self):
        while True:
            if self.__stop_event.is_set():
                break

            if self._media_player.get_finished():
                self.play_next_song()
            time.sleep(0.1)