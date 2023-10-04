def getMaxTile(grid):
    maxTile = 0

    for x in range(4):
        for y in range(4):
            maxTile = max(maxTile, grid[x][y])

    return maxTile


def getAvailableCells(grid):
    cells = []

    for x in range(4):
        for y in range(4):
            if grid[x][y] == 0:
                cells.append((x,y))

    return len(cells)

def getCellsNum(grid):
    cells = []
    sum = 0

    for x in range(4):
        for y in range(4):
            if grid[x][y] != 0:
                cells.append(grid[x][y])
    for i in range(len(cells)):
        sum = sum+cells[i]



    return sum


if __name__ == '__main__':
    grid = [[0, 0, 0, 32],
            [0, 0, 0, 0],
            [2, 2, 128, 0],
            [4, 8, 0, 0]]
    largestNum = getMaxTile(grid)
    print(largestNum)
    empty = getAvailableCells(grid)
    print(empty)
    sum = getCellsNum(grid)
    print(sum)
    total = largestNum + 2* sum + 3 * empty










