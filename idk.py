# Your code here
# You can import some modules or create additional functions
from typing import List, Tuple


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


class Checker:
    class TaskNode:
        def __init__(self, type, x: int, y: int):
            self.x = x
            self.y = y
            self.type = type  # type: int
            self.dist = 0
            self.queue = Queue()  # type: Queue
            self.visited = False

        def exit(self):
            self.type = 2

        def start(self):
            self.type = 3

        def is_start(self):
            return self.type == 2

        def is_end(self):
            return self.type == 3

        def visit(self, dist):
            self.visited = True
            self.dist = dist + 1

        def peek(self):
            if self.visited:
                return None
            return self

    def __init__(self, data: list, start: Tuple[int, int], end: Tuple[int, int]):
        if data is None:
            raise ValueError('Data must not be none')

        self.height = len(data)
        self.width = len(data[0])  # Assume data is square
        self.nodes = []  # type: List[TaskNode]
        self.queue = Queue()  # type: Queue
        i = 0
        for nodes in data:
            self.nodes.append([])
            j = 0
            for node in nodes:
                self.nodes[i].append(Checker.TaskNode(node, j, i))
                j += 1
            i += 1

        if start is None or start == () or end is None or end == () or start == end:
            raise ValueError('Start and end must be two distinct tuples '
                             'representing position of start and end (x,y)')

        if not self.is_in_bounds(*start):
            raise IndexError('Start out of bounds')

        if not self.is_in_bounds(*end):
            raise IndexError('End out of bounds')

        self.get_node(*start).start()
        self.get_node(*end).exit()
        self.start = start  # type: TaskNode
        self.exit = end  # type: TaskNode
    def print(self):
        for nodes in self.nodes:
            for node in nodes:
                print(node.dist, end="  , ")
            print()

    def is_in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def get_node(self, x, y) -> TaskNode:
        if not self.is_in_bounds(x, y):
            return None

        return self.nodes[y][x]

    def node_neighbrohood(self, node: TaskNode) -> List[TaskNode]:
        ret = []

        test = self.get_node(node.x + 1, node.y)
        if test is not None and test.type != 1:
            ret.append(test)

        test = self.get_node(node.x - 1, node.y)
        if test is not None and test.type != 1:
            ret.append(test)

        test = self.get_node(node.x, node.y + 1)
        if test is not None and test.type != 1:
            ret.append(test)

        test = self.get_node(node.x, node.y - 1)
        if test is not None and test.type != 1:
            ret.append(test)

        return ret

    def walk_neighbrohood(self, node: TaskNode):
        ret = []

        neigb = self.node_neighbrohood(node)
        for nnode in neigb:
            if nnode.peek() is not None:
                ret.append(nnode)
                nnode.visit(node.dist)

        return ret

    def walk(self):
        node = self.get_node(*self.start)
        node.visited = True
        exit = self.get_node(*self.exit)

        while node is not None:
            neigb = self.walk_neighbrohood(node)
            #print(len(neigb))
            if self.exit in neigb:
                return
            for wnode in neigb:
                self.queue.enqueue(wnode)
            node = self.queue.dequeue()
        #print(self.get_node(*self.exit).dist)

    @staticmethod
    def node2letter(start: TaskNode, end: TaskNode):
        if start is None or end is None:
            return ""
        dx, dy = end.x - start.x, end.y - start.y
        if abs(dx) + abs(dy) > 1:
            return ""

        if dx == -1:
            return "E"

        if dx == 1:
            return "W"

        if dy == 1:
            return "N"

        if dy == -1:
            return "S"

        return ""

    def previous(self, node: TaskNode):
        if node is None:
            return None
        neigb = self.node_neighbrohood(node)
        for tnode in neigb:
            if tnode.dist - node.dist == -1:
                return tnode
        return None

    def backtrack(self):
        ret = ""
        node = self.get_node(*self.exit)
        while node != self.get_node(*self.start):
            tnode = self.previous(node)
            ret += self.node2letter(node, tnode)
            node = tnode
            if node is None:
                return ""
        return ret[::-1]


def checkio(data: list) -> str:
    checker = Checker(data, (1, 1), (10, 10))
    checker.walk()
    #checker.print()
    ret = checker.backtrack()
    print(ret)
    return ret


if __name__ == '__main__':

    # This code using only for self-checking and not necessary for auto-testing
    def check_route(func, labyrinth):
        MOVE = {"S": (1, 0), "N": (-1, 0), "W": (0, -1), "E": (0, 1)}
        # copy maze
        route = func([row[:] for row in labyrinth])
        pos = (1, 1)
        goal = (10, 10)
        for i, d in enumerate(route):
            move = MOVE.get(d, None)
            if not move:
                print("Wrong symbol in route")
                return False
            pos = pos[0] + move[0], pos[1] + move[1]
            if pos == goal:
                return True
            if labyrinth[pos[0]][pos[1]] == 1:
                print("Player in the pit")
                return False
        print("Player did not reach exit")
        return False


    # These assert are using only for self-testing as examples.
    assert check_route(checkio, [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1],
        [1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]), "First maze"
    assert check_route(checkio, [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]), "Empty maze"
    assert check_route(checkio, [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]), "Up and down maze"
    assert check_route(checkio, [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]), "Dotted maze"
    assert check_route(checkio, [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1],
        [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]), "Need left maze"
    assert check_route(checkio, [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]), "The big dead end."
    print("The local tests are done.")
