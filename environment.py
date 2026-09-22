import random


class Environment:

    EMPTY = "empty"
    FIRE = "fire"
    COLLAPSE = "collapse"
    SURVIVOR = "survivor"
    EXIT = "exit"

    def __init__(self, size):
        self.size = size
        self.grid = [
            [self.EMPTY for _ in range(size)]
            for _ in range(size)
        ]

        self.agent_position = (size - 1, 0)

        self.generate_environment()

    def generate_environment(self):

        # Exit
        self.grid[self.size - 1][0] = self.EXIT

        # Fixed survivor
        self.grid[2][6] = self.SURVIVOR

        # Fixed hazards for predictable testing
        self.grid[1][3] = self.FIRE
        self.grid[4][5] = self.FIRE

        self.grid[3][2] = self.COLLAPSE
        self.grid[5][6] = self.COLLAPSE

    def is_inside(self, row, col):
        return (
            0 <= row < self.size and
            0 <= col < self.size
        )

    def get_cell(self, row, col):

        if not self.is_inside(row, col):
            return None

        return self.grid[row][col]