from typing import Tuple, List
from util.structs import Queue


class HauntedTile:
    def __init__(self, parent, dirs: str, x: int, y: int, stephen=False, ghost=False):
        self.parent = parent  # type: HauntedHouse
        self.x = x
        self.y = y
        self.doors = 4 - len(dirs)
        self.north = "N" not in dirs and 0 <= y - 1
        self.east = "E" not in dirs and 4 > x + 1
        self.south = "S" not in dirs and 4 > y + 1
        self.west = "W" not in dirs and 0 <= x - 1
        self._ghost = ghost
        self._stephen = stephen
        self.old = None
        self.visited = False

    def neighbrohood_tuples(self):
        ret = []
        if self.north:
            ret.append((self.x, self.y - 1))
        if self.east:
            ret.append((self.x + 1, self.y))
        if self.south:
            ret.append((self.x, self.y + 1))
        if self.west:
            ret.append((self.x - 1, self.y))

        return ret

    def block(self, blocked=""):
        self.old = (self.north, self.east, self.south, self.west)
        self.north, self.east, self.south, self.west = "N" in blocked, "E" in blocked, \
                                                       "S" in blocked, "W" in blocked

    def unblock(self):
        if self.old is None:
            return
        self.north, self.east, self.south, self.west = self.old
        self.old = None

    def ghost(self, val=None):
        if val is not None:
            self._ghost = val
        return self.ghost

    def stephen(self, val=None):
        if val is not None:
            self._stephen = val
        return self.stephen

    def visit(self, val=None):
        if val is not None:
            self.visited = val
        return self.visited




class Path:
    def __init__(self):
        self.positions = []  # type: List[Tuple[int, int]]
        self.distances = 0  # type: int

    def has(self, pos: Tuple[int, int]) -> bool:
        return pos in self.positions

    def copy(self):
        ret = Path()
        for pos in self.positions:
            ret.add(pos)
        return ret

    def add(self, pos: Tuple[int, int]):
        self.positions.append(pos)
        self.distances += 1


class HauntedHouse:
    def __init__(self, blocked: List[str], stephen: Tuple[int, int], ghost: Tuple[int, int]):
        self.blocked = blocked
        self.stephen = stephen
        self.ghost = ghost
        self.map = []  # type: List[HauntedTile]
        for y in range(0, 4):
            for x in range(0, 4):
                self.map.append(HauntedTile(self, blocked[y * 4 + x], x, y))

        self.tile(*stephen).stephen(True)
        self.tile(*ghost).ghost(True)
        self.paths = []

    def tile(self, x: int, y: int) -> HauntedTile:
        if 0 <= x < 4 and 0 <= y < 4:
            return self.map[x + y * 4]
        return None

    def compute_all_paths(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Path]:
        self.compute_all_paths_hlpr(start, end, Path())
        paths = self.paths
        self.paths = []
        return paths

    def compute_all_paths_hlpr(self, start: Tuple[int, int], end: Tuple[int, int], path_thus_far: Path):
        print(start)
        path_thus_far.add(start)
        if start == end:
            self.paths.append(path_thus_far)
            return

        neighbrohood = self.tile(*start).neighbrohood_tuples()
        for neighbro in neighbrohood:
            if not path_thus_far.has(neighbro):
                self.compute_all_paths_hlpr(neighbro, end, path_thus_far.copy())


if __name__ == '__main__':
    print(range(0,4))
    blk = ["","S","S","","E","NW","NS","","E","WS","NS","","","N","N",""]
    hh = HauntedHouse(blk,(3,3),(0,0))
    ret = hh.compute_all_paths((3,3),(0,0))
    for r in ret:
        print("Path: ")
        for n in r.positions:
            print(n, end=", ")
        print()

