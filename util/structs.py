
class Queue:
    class QueueNode:
        def __init__(self, obj):
            self.nextNode = None  # type: QueueNode
            self.held = obj

    def __init__(self):
        self.start = None  # type: QueueNode
        self.end = None  # type: QueueNode

        self.count = 0

    def enqueue(self, obj):
        self.count += 1
        if self.start is None:
            self.start = Queue.QueueNode(obj)
            self.end = self.start
        else:
            self.end.nextNode = Queue.QueueNode(obj)
            self.end = self.end.nextNode

    def dequeue(self):
        self.count -= 1
        if self.start is None:
            return None
        else:
            ret = self.start
            if self.start is self.end:
                self.start = None
                self.end = None
            else:
                self.start = self.start.nextNode
            return ret.held

    def empty(self):
        return self.size() == 0

    def size(self):
        return self.count