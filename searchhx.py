from copy import deepcopy
from random import randint
import numpy as np

# UP=1 DOWN=2 LEFT=3 RIGHT=4
code = [UP, DOWN, LEFT, RIGHT] = [0, 1, 2, 3]


class Board:
    def __init__(self, size=4):
        self.size = size
        self.map = [[0] * self.size for i in range(self.size)]

    def give_spot_value(self, coor, value):
        self.map[coor[0]][coor[1]] = value

    # Return all the empty cells
    def get_empty_spots(self):
        spots = []
        array = np.array(self.map)
        np.sum(array == 0)
        for x in range(self.size):
            for y in range(self.size):
                if self.map[x][y] == 0:
                    spots.append((x, y))
        return spots

    # Return the tile with maximum value
    def max_value_tile(self):
        max_value = 0
        for x in range(self.size):
            for y in range(self.size):
                maxTile = max(max_value, self.map[x][y])
        return max_value

    # Make a Deep Copy of This Object
    def duplicate(self):
        duplicate = Board()
        duplicate.size = self.size
        duplicate.map = deepcopy(self.map)
        return duplicate

    # Merge Tiles
    def combine(self, spots):
        if len(spots) > 1:
            i = 0
            while True:
                if spots[i] == spots[i + 1]:
                    spots[i] *= 2
                    del spots[i + 1]

                i += 1
                if i >= len(spots) - 1:
                    break
        else:
            return spots

    # Move the Grid
    def move(self, key):
        key = int(key)

        if key == UP:
            r = range(self.size)
            moved = False

            for j in range(self.size):
                cells = []

                for i in r:
                    cell = self.map[i][j]

                    if cell != 0:
                        cells.append(cell)

                self.combine(cells)

                # pop the first item in cells in order
                for i in r:
                    value = cells.pop(0) if cells else 0

                    if self.map[i][j] != value:
                        moved = True

                    self.map[i][j] = value

            return moved

        if key == DOWN:
            r = range(self.size - 1, -1, -1)

            moved = False

            for j in range(self.size):
                cells = []

                for i in r:
                    cell = self.map[i][j]

                    if cell != 0:
                        cells.append(cell)

                self.combine(cells)

                # pop the first item in cells in order
                for i in r:
                    value = cells.pop(0) if cells else 0

                    if self.map[i][j] != value:
                        moved = True

                    self.map[i][j] = value

            return moved

        if key == LEFT:
            r = range(self.size)

            moved = False

            for i in range(self.size):
                cells = []

                for j in r:
                    cell = self.map[i][j]

                    if cell != 0:
                        cells.append(cell)

                self.combine(cells)

                for j in r:
                    value = cells.pop(0) if cells else 0

                    if self.map[i][j] != value:
                        moved = True

                    self.map[i][j] = value

            return moved

        if key == RIGHT:
            r = range(self.size - 1, -1, -1)

            moved = False

            for i in range(self.size):
                cells = []

                for j in r:
                    cell = self.map[i][j]

                    if cell != 0:
                        cells.append(cell)

                self.combine(cells)

                for j in r:
                    value = cells.pop(0) if cells else 0

                    if self.map[i][j] != value:
                        moved = True

                    self.map[i][j] = value

            return moved

    # Return All Available Moves
    def get_all_Moves(self, key=range(4)):
        moves = []

        for x in key:
            gridCopy = self.duplicate()

            if gridCopy.move(x):
                moves.append(x)

        return moves

    # check if pos were out of grid's bound
    # return 1 if out of bound, 0 if not
    def crossBound(self, pos):
        return pos[0] < 0 or pos[0] >= self.size or pos[1] < 0 or pos[1] >= self.size

    # get the value of a certain tile
    def getCellValue(self, pos):
        if not self.crossBound(pos):
            return self.map[pos[0]][pos[1]]
        else:
            return None

    # whether monotonic
    def isMonotonic(self, array):
        isNotIncreasing = True
        isNotDecreasing = True
        for _ in range(1,len(array)):
          if array[_]>array[_-1]:
            isNotIncreasing = False
          if array[_]<array[_-1]:
            isNotDecreasing = False
        return isNotDecreasing or isNotIncreasing


class Action(Board):
    # stage is the current matrix
    def start_action(self, action):
        self.first_action= action
        self.depth = 0
        move = self.optimal()
        return move

    def optimal(self):
        opt_move = None
        max_value = -999999999
        # iterate every available moves
        for move in self.first_action.get_all_Moves():
            # clone of the current matrix
            next_action = self.first_action.duplicate()
            # move to next matrix
            # nextStage changes
            next_action.move(move)

            value = self.MIN(next_action, -999999999, 999999999)
            if max_value < value:
                opt_move = move
            max_value = max(max_value, value)

        return opt_move

    def MAX(self, action, a, b):
        self.depth = self.depth + 1
        score = -999999999
        # All availabble moves
        moves = action.get_all_Moves()
        if not moves or self.depth > 8:
            self.depth = self.depth - 1
            return self.calculation(action)

        for move in moves:
            next_action = action.duplicate()
            next_action.move(move)
            score = max(score, self.MIN(next_action, a, b))
            a = max(score, a)
            if a > b:
                return score
        # value for max node is decided
        # back to its parent min node
        self.depth = self.depth - 1
        return score

    def MIN(self, action, a, b):
        self.depth = self.depth + 1
        # pos where are empty
        score = 999999999
        moves = action.get_empty_spots()
        if not moves or self.depth > 8:
            self.depth = self.depth - 1
            return self.calculation(action)

        for move in moves:
            # value=2,4
            for value in range(2, 5, 2):
                next_action = action.duplicate()
                next_action.give_spot_value(move, value)
                nextV = self.MAX(next_action, a, b)
                score = min(score, nextV)
                b = min(b, score)
                if b < a:
                    return score

        self.depth = self.depth - 1
        return score

    def calculation(self, stage):
        monotony = 0
        combination = 0
        difference = 0

        # calculating smoothness
        for i in range(3):
            for j in range(4):
                difference = difference + abs(stage.map[i + 1][j] - stage.map[i][j])

        for j in range(3):
            for i in range(4):
                difference = difference + abs(stage.map[i][j] - stage.map[i][j + 1])
        # calculating merging
        for i in range(3):
            for j in range(4):
                if stage.map[i + 1][j] == stage.map[i][j]:
                    combination += 1

        for j in range(3):
            for i in range(4):
                if stage.map[i][j] == stage.map[i][j + 1]:
                    combination += 1

        array = np.array(stage.map)
        for x in range(0, 4, 1):
            if stage.isMonotonic(array[x, :]):
                monotony += 1
        for y in range(0, 4, 1):
            if stage.isMonotonic(array[:, y]):
                monotony+= 1

        zero = len(stage.get_empty_spots())
        max = stage.max_value_tile()

        return monotony+zero+2*combination-0.01*difference+0.00001*max


def NextMove(Grid, step):
    action = Action()
    action.map = Grid
    move = action.start_action(action)
    step = step+1
    return move
