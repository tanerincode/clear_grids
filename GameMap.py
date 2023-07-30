class GameMap:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.data = [[0]*w for _ in range(h)]

    def __lt__(self, other):
        return id(self) < id(other)

    @staticmethod
    def parse(lines):
        # first line should contain grid dimensions
        w, h = map(int, lines[0].split())

        # the rest of the lines are the grid
        level_lines = lines[1:]

        # Initialize a GameMap with the given dimensions
        m = GameMap(w, h)

        # Fill in the cells of the GameMap
        for y in range(h):
            row = list(map(int, level_lines[y].split()))
            for x in range(w):
                m.data[y][x] = row[x]

        return m

    def get_copy(self):
        copy = GameMap(self.w, self.h)
        copy.data = [row.copy() for row in self.data]
        return copy

    def move(self, source, target):
        self.data[target[0]][target[1]] -= self.data[source[0]][source[1]]
        self.data[source[0]][source[1]] = 0

    def is_empty(self):
        for row in self.data:
            if any(cell != 0 for cell in row):
                return False
        return True

    @staticmethod
    def load_from_file(filePath):
        with open(filePath, 'r') as f:
            lines = f.readlines()
            m = GameMap.parse(lines)
            return m