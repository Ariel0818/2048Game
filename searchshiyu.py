from copy import deepcopy
from random import randint
from math import ceil
import numpy as np
from datetime import datetime



vecIndex = [0, 1, 2, 3]


class Grid:
    def __init__(self, size=4):
        self.shape = 4
        self.trace = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]   # trace


    def clone(self):
        gridClone = Grid()
        gridClone.trace = deepcopy(self.trace)
        gridClone.shape = 4
        return gridClone


    def setValue(self, pos, num):
        self.trace[pos[0]][pos[1]] = num


    def EmptyCells(self):
        cells = []
        for x in range(4):
            for y in range(4):
                if self.trace[x][y] == 0:
                    cells.append((x, y))
        return cells

# operation
    # Merge Tiles
    def merge(self, cells):
        if len(cells) <= 1:
            return cells
        i = 0
        while i < len(cells) - 1:
            if cells[i] == cells[i + 1]:
                temp = cells.pop(i+1)     # （41
                cells[i] = cells[i] + temp
            i += 1


    def moveUp(self, up):

        # down: range(3,-1,-1):3,2,1,0  up: range(4): 0,1,2,3
        moved = False
        for j in range(self.shape):
            points = []
            for i in range(self.shape):
                point = self.trace[i][j]
                if point != 0:
                    points.append(point)

            self.merge(points)
            # pop the first item in cells in order

            for i in range(self.shape):
                if points:
                    value = points[0]
                    del points[0]
                else:
                    value = 0

                if self.trace[i][j] != value:
                    moved = True

                self.trace[i][j] = value
        return moved


    def moveDown(self, down):
        # down: range(3,-1,-1):3,2,1,0  up: range(4): 0,1,2,3

        moved = False
        for j in range(self.shape):
            points = []
            for i in range(3, -1, -1):
                point = self.trace[i][j]
                if point != 0:
                    points.append(point)
            self.merge(points)
            # pop the first item in cells in order
            for i in range(3, -1, -1):
                if points:
                    value = points[0]
                    del points[0]
                else:
                    value = 0

                if self.trace[i][j] != value:
                    moved = True
                self.trace[i][j] = value
        return moved


    # move left or right

    # return true or false

    def moveLeft(self, left):
        # right: range(3,-1,-1):3,2,1,0  left: range(4): 0,1,2,3

        moved = False
        for i in range(4):
            points = []
            for j in range(4):
                point = self.trace[i][j]
                if point != 0:
                    points.append(point)
            self.merge(points)
            for j in range(4):
                if points:
                    value = points[0]
                    del points[0]
                else:
                    value = 0

                if self.trace[i][j] != value:
                    moved = True
                self.trace[i][j] = value
        return moved


    def moveRight(self, right):
        # right: range(3,-1,-1):3,2,1,0  left: range(4): 0,1,2,3
        moved = False
        for i in range(self.shape):
            points = []
            for j in range(3, -1, -1):
                cell = self.trace[i][j]
                if cell != 0:
                    points.append(cell)
            self.merge(points)
            for j in range(3, -1, -1):
                if points:
                    value = points[0]
                    del points[0]
                else:
                    value = 0
                if self.trace[i][j] != value:
                    moved = True
                self.trace[i][j] = value
        return moved


    def move(self, dir):
        dir = int(dir)
        if dir == 0:  # up
            return self.moveUp(True)
        if dir == 1:  # down
            return self.moveDown(True)
        if dir == 2:  # left
            return self.moveLeft(True)
        if dir == 3:  # right
           return self.moveRight(True)


    # Return All Available Moves
    def PossibleSteps(self, dirs=vecIndex):
        availableStep = []
        for x in dirs:
            Copy = self.clone()

            if Copy.move(x) is True:
                availableStep.append(x)
        return availableStep




class Play2048(Grid):

    # stage is the current matrix

    def NextStage(self, stage):
        self.orignial = stage
        neginf = -float('inf')
        self.d = 0
        NextStep = None
        for move in self.orignial.PossibleSteps():
            next = self.orignial.clone()
            next.move(move)
            value = self.min(next, -float('inf'), float('inf'))
            if value > neginf:
                neginf = value
                NextStep = move

        move = NextStep

        return move



    def max(self, stage, Alpha, Beta):
        self.d += 1
        # All availabble moves
        Step = stage.PossibleSteps()
        value = -float('inf')

        for move in Step:
            nextStage = stage.clone()
            nextStage.move(move)
            temp = self.min(nextStage, Alpha, Beta)
            value = max(value, temp)
            Alpha = max(value, Alpha)
            if Alpha > Beta:
                return value

        if not Step:
            self.d -= 1
            return self.CALCULATE(stage)
        if self.d > 40:
            self.d -= 1
            return self.CALCULATE(stage)



        # value for max node is decided
        # back to its parent min node

        self.d -= 1
        return value


    def min(self, stage, Alpha, Beta):
        self.d = self.d + 1
        # pos where are empty
        Step = stage.EmptyCells()
        nextStage = None
        if not Step :
            self.d = self.d - 1
            return self.CALCULATE(stage)
        if self.d > 40:
            self.d = self.d - 1
            return self.CALCULATE(stage)

        new = float('inf')
        for move in Step:
            # value=2,4
            for value in [2, 4]:
                nextStage = stage.clone()
                nextStage.setValue(move, value)
                nextValue = self.max(nextStage, Alpha, Beta)
                new = min(new, nextValue)
                Beta = min(Beta, new)
                if Beta < Alpha:
                    return new


        self.d = self.d - 1
        return new


    def CALCULATE(self, grid):
        sum = []
        for i in range(4):
            A = grid.trace[i]
            B = sorted(A)
            result = (B == A or B == A[::-1])
            sum.append(result)
        for j in range(4):
            array = np.array(grid.trace)
            B = array[:, j]
            b = list(B)
            C = sorted(b)
            result2 = (C == b or C == b[::-1])
            sum.append(result2)

        mono = 0
        for k in range(len(sum)):
           if sum[k] == True:
                mono = mono + 1

        em = grid.EmptyCells()
        empty = len(em)

        diff = 0
        merge = 0
        for i in range(3):
            for j in range(4):
                diff = diff + abs(grid.trace[i + 1][j] - grid.trace[i][j])
                if grid.trace[i+1][j] == grid.trace[i][j]:
                    merge = merge+1

        for j in range(3):
            for i in range(4):
                diff = diff + abs(grid.trace[i][j] - grid.trace[i][j + 1])
                if grid.trace[i][j] == grid.trace[i][j+1]:
                    merge = merge+1


        return mono + empty - diff * 0.01 + merge


def getChild(grid, dir):
	temp = grid.clone()
	temp.move(dir)
	return temp


#Gets all the Children of a node
def children(grid):
	children = []
	for move in grid.getAvailableMoves():
		children.append(getChild(grid, move))
	return children


class BaseAI:
    def getMove(self, grid):
        pass


class BaseDisplayer:
    def __init__(self):
        pass

    def display(self, grid):
        pass


def NextMove(Grid, step):
    import numpy as np
    grid = Play2048()
    grid.trace = Grid
    move = grid.NextStage(grid)
    return move

