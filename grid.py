from copy import deepcopy
vecIndex = [UP, DOWN, LEFT, RIGHT] = range(4)

def clone(grid):  # grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    gridcopy = deepcopy(grid)
    return gridcopy


def setCallVelue(grid, pos, value):
    grid[pos[0]][pos[1]] = value  # pos[0] 是行，pos[1]是列 pos[1 ,1 ] 表示取第2行第2列的数字赋值


def getAvailableCells(grid):
    cells = []
    for x in range(4):
        for y in range(4):
            if grid[x][y] == 0:
                cells.append((x, y)) # [(0, 0), (0, 1), (0, 3), (1, 2), (1, 3), (2, 0), (2, 1), (2, 2), (2, 3), (3, 0), (3, 1), (3, 2), (3, 3)]
    return cells

def merge(cells):
    if len(cells) <= 1:
        return cells

    i = 0
    while i < len(cells) - 1:  # len(cell) = 2  0<1
        if cells[i] == cells[i+1]:  # cells[0] == cells[1]
            cells[i] *= 2  # cells[0]*2
            del cells[i+1]

        i += 1

def moveUD(down, grid):
    r = range(3, -1, -1) if down else range(4)
    # range(3,-1,-1) ->  range(start, stop [, step]) 不会包含最后的stop值

    moved = False

    for j in range(4):  # j = 0,1,2,3
        cells = []

        for i in r:  # i = 3，2，1，0
            cell = grid[i][j]  # cell = grid[3][0]

            if cell != 0:
                cells.append(cell)  # 把有值的格子都合并在一起
        merge(cells)
        for i in r:
            value = cells.pop(0) if cells else 0

            if grid[i][j] != value:
                moved = True

            grid[i][j] = value

    return moved


def moveLR(right, grid):  # 如果左、右移动可以合并才会输出true
    r = range(3, -1, -1) if right else range(4)

    moved = False

    for i in range(4):
        cells = []

        for j in r:
            cell = grid[i][j]

            if cell != 0:
                cells.append(cell)

        merge(cells)

        for j in r:
            value = cells.pop(0) if cells else 0  # 删除第一个元素pop(0)

            if grid[i][j] != value:
                moved = True

            grid[i][j] = value

    return moved


def move(dir, grid):
    dir = int(dir)

    if dir == UP:  # 0
        return moveUD(False, grid)
    if dir == DOWN:  # 1
        return moveUD(True, grid)
    if dir == LEFT:  # 2
        return moveLR(False, grid)
    if dir == RIGHT:  # 3
        return moveLR(True, grid)


def getAvailableMoves(grid,dirs = vecIndex):
    availableMoves = []

    for x in dirs:
        gridCopy = clone(grid)

        if gridCopy.move(x):
            availableMoves.append(x)

    return availableMoves

if __name__ == '__main__':
    grid = [[0, 0, 0, 0],
            [0, 0, 0, 0],
            [2, 2, 0, 0],
            [4, 8, 0, 0]]

    a = move(3, grid)
    print(a)

def NextMove(grid, step):


