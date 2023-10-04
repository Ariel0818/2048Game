from BaseAI_3 import BaseAI
from Grid_3 import Grid
from copy import deepcopy
from random import randint

directionVectors = (UP_VEC, DOWN_VEC, LEFT_VEC, RIGHT_VEC) = ((-1, 0), (1, 0), (0, -1), (0, 1))
vecIndex = [UP, DOWN, LEFT, RIGHT] = range(4)



class ComputerAI(BaseAI):
    def getMove(self, grid):
        cells = grid.getAvailableCells()

        return cells[randint(0, len(cells) - 1)] if cells else None

class BaseAI:
    def getMove(self, grid):
        pass


class Grid:
    def __init__(self, size = 4):
        self.size = size
        self.map = [[0] * self.size for i in range(self.size)]  # 建立了一个4行4列的二维矩阵
        # map = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

    # Make a Deep Copy of This Object
    def clone(self):
        gridCopy = Grid()
        gridCopy.map = deepcopy(self.map)
        gridCopy.size = self.size

        return gridCopy

    # Insert a Tile in an Empty Cell
    def insertTile(self, pos, value):
        self.setCellValue(pos, value)

    def setCellValue(self, pos, value):
        self.map[pos[0]][pos[1]] = value  # pos[0] 是行，pos[1]是列 pos[1 ,1 ] 表示取第2行第2列的数字赋值

    # Return All the Empty c\Cells
    def getAvailableCells(self):
        cells = []

        for x in range(self.size):
            for y in range(self.size):
                if self.map[x][y] == 0:
                    cells.append((x,y))

        return cells

    # Return the Tile with Maximum Value
    def getMaxTile(self):
        maxTile = 0

        for x in range(self.size):
            for y in range(self.size):
                maxTile = max(maxTile, self.map[x][y])

        return maxTile

    # Check If Able to Insert a Tile in Position
    def canInsert(self, pos):
        return self.getCellValue(pos) == 0

    # Move the Grid
    def move(self, dir):
        dir = int(dir)

        if dir == UP:
            return self.moveUD(False)
        if dir == DOWN:
            return self.moveUD(True)
        if dir == LEFT:
            return self.moveLR(False)
        if dir == RIGHT:
            return self.moveLR(True)

    # Move Up or Down
    def moveUD(self, down):
        r = range(self.size -1, -1, -1) if down else range(self.size)
        # range(3,-1,-1) ->  range(start, stop [, step]) 不会包含最后的stop值

        moved = False

        for j in range(self.size):
            cells = []

            for i in r:  # i = 3，2，1，0
                cell = self.map[i][j]

                if cell != 0:
                    cells.append(cell)

            self.merge(cells)

            for i in r:
                value = cells.pop(0) if cells else 0

                if self.map[i][j] != value:
                    moved = True

                self.map[i][j] = value

        return moved

    # move left or right
    def moveLR(self, right):
        r = range(self.size - 1, -1, -1) if right else range(self.size)

        moved = False

        for i in range(self.size):
            cells = []

            for j in r:
                cell = self.map[i][j]

                if cell != 0:
                    cells.append(cell)

            self.merge(cells)

            for j in r:
                value = cells.pop(0) if cells else 0

                if self.map[i][j] != value:
                    moved = True

                self.map[i][j] = value

        return moved

    # Merge Tiles
    def merge(self, cells):
        if len(cells) <= 1:
            return cells

        i = 0

        while i < len(cells) - 1:
            if cells[i] == cells[i+1]:
                cells[i] *= 2

                del cells[i+1]

            i += 1



    # Return All Available Moves
    def getAvailableMoves(self, dirs = vecIndex):
        availableMoves = []

        for x in dirs:
            gridCopy = self.clone()

            if gridCopy.move(x):
                availableMoves.append(x)

        return availableMoves



class PlayerAI(Grid):
    H = [[65536, 32768, 16384, 8192], [512, 1024, 2048, 4096], [256, 128, 64, 32], [2, 4, 8, 16]]

    # stage is the current matrix
    def getMove(self, stage, step):
        self.initialStage = stage
        self.ALPHA = -999999999
        self.BETA = 999999999
        self.deep = 0
        move = self.SELECT(step)
        return move

    def SELECT(self,step):
        maxV = -999999999
        selectedMove = None
        nextStage = None
        # iterate every available moves
        for move in self.initialStage.getAvailableMoves():
            # clone of the current matrix
            nextStage = self.initialStage.clone()
            # move to next matrix
            # nextStage changes
            nextStage.move(move)

            value = self.MIN(nextStage, -999999999, 999999999,step)
            if maxV < value:
                maxV = value
                selectedMove = move
        return selectedMove

    def MAX(self, stage, a, b,step):
        self.deep = self.deep + 1
        # All availabble moves
        moves = stage.getAvailableMoves()
        nextStage = None
        if not moves or self.deep > step:
            self.deep = self.deep - 1
            return self.CALCULATE(stage)
        average = -999999999
        for move in moves:
            nextStage = stage.clone()
            nextStage.move(move)
            average = max(average, self.MIN(nextStage, a, b,step))
            a = max(average, a)
            if a > b:
                return average
        # value for max node is decided
        # back to its parent min node
        self.deep = self.deep - 1
        return average

    def MIN(self, stage, a, b,step):
        self.deep = self.deep + 1
        # pos where are empty
        moves = stage.getAvailableCells()
        nextStage = None
        if not moves or self.deep > step:
            self.deep = self.deep - 1
            return self.CALCULATE(stage)
        average = 999999999
        for move in moves:
            # value=2,4
            for value in range(2, 5, 2):
                nextStage = stage.clone()
                nextStage.setCellValue(move, value)
                nextV = self.MAX(nextStage, a, b)
                average = min(average, nextV)
                b = min(b, average)
                if b < a:
                    return average

        self.deep = self.deep - 1
        return average

    def CALCULATE(self, stage):
        d = self.deep + 1
        diff = 0
        combine = 0
        adding = 0
        order = 0
        # 0,1,2,3
        for x in range(0, 4, 1):
            for y in range(0, 4, 1):
                adding = adding + stage.map[x][y]
                if stage.map[x][y] == 0:
                    pass
                order = order + self.H[x][y] * stage.map[x][y]
                if (x == 0) or (x == 1) or (x == 2):
                    poss = x - 1
                    diff = diff + (stage.map[x][y] - stage.map[poss][y])
                    if stage.map[x][y] == stage.map[poss][y]:
                        combine = combine + stage.map[x][y]
                if x == 4:
                    poss = x + 1
                    diff = diff + (stage.map[x][y] - stage.map[poss][y])
                    if stage.map[x][y] == stage.map[poss][y]:
                        combine = combine + stage.map[x][y]
                if (y == 0) or (y == 1) or (y == 2):
                    poss = y - 1
                    diff = diff + (stage.map[x][y] - stage.map[x][poss])
                    if stage.map[x][y] == stage.map[x][poss]:
                        combine = combine + stage.map[x][y]
                if y == 4:
                    poss = y + 1
                    diff = diff + (stage.map[x][y] - stage.map[x][poss])
                    if stage.map[x][y] == stage.map[x][poss]:
                        combine = combine + stage.map[x][y]
        return 2 * d * order + d * adding + d * diff + d * combine


def NextMove(grid):
    Grid = PlayerAI()
    Grid.map = grid
    move = Grid.getMove(Grid)

    return move