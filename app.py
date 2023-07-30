from GameMap import GameMap
from heapq import heappush, heappop


class Game:
    DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # R, L, D, U
    DIR_TO_STR = {(0, 1): 'R', (0, -1): 'L', (1, 0): 'D', (-1, 0): 'U'}

    @staticmethod
    def get_distance(pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    @staticmethod
    def get_next_pos(pos, direction, value):
        return (pos[0] + direction[0] * value, pos[1] + direction[1] * value)

    @staticmethod
    def is_valid_move(map, pos):
        x, y = pos
        return 0 <= x < map.h and 0 <= y < map.w and map.data[x][y] > 0

    @staticmethod
    def get_possible_moves(map):
        moves = []
        for i in range(map.h):
            for j in range(map.w):
                value = map.data[i][j]
                if value > 0:
                    for direction in Game.DIRECTIONS:
                        next_pos = Game.get_next_pos((i, j), direction, value)
                        if Game.is_valid_move(map, next_pos):
                            moves.append(((i, j), next_pos, direction))
        return moves

    @staticmethod
    def solve(map):
        start = map.get_copy()
        queue = [(0, start, [])]
        visited = set([start])
        while queue:
            _, current, path = heappop(queue)
            if current.is_empty():
                return path
            for source, target, direction in Game.get_possible_moves(current):
                new_map = current.get_copy()
                new_map.move(source, target)
                if new_map not in visited:
                    new_cost = (Game.get_distance(source, target) +
                                Game.get_distance(target, Game.get_next_pos(target, direction,
                                                                            -new_map.data[target[0]][target[1]])))

                    heappush(queue, (new_cost, new_map, path + [(source, target, direction)]))
                    visited.add(new_map)
        return None

    @staticmethod
    def main(filePath):
        print(f"Loading level from {filePath}")
        current_map = GameMap.load_from_file(filePath)
        solution = Game.solve(current_map)
        if solution is not None:
            print("Solution found:")
            for source, target, direction in solution:
                print(f"{source[1]} {source[0]} {Game.DIR_TO_STR[direction]} -")
        else:
            print("No solution found")


if __name__ == "__main__":
    level_file_path = f"./Levels/0XX/1.txt"
    Game.main(level_file_path)
