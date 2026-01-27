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
    
if __name__ == "__main__":
    print("--- QUEUE MEMORY TEST ---")
    import sys
    q = Queue()

    num_songs = 10000
    for i in range(0, num_songs):
        q.enqueue("TEST SONG by TEST ARTIST")
    print(f"{sys.getsizeof(q._queue) * 0.000001:.2f}MB with {q.size():,} items")
    print(f"~{q.size() * 5 / 60:.1f} hours of listening")