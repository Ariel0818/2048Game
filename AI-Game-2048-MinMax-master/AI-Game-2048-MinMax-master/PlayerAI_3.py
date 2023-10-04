from BaseAI_3 import BaseAI
from Grid_3 import Grid
from copy import deepcopy
import numpy as np

directionVectors = (UP_VEC, DOWN_VEC, LEFT_VEC, RIGHT_VEC) = ((-1, 0), (1, 0), (0, -1), (0, 1))
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
vecIndex = [0, 1, 2, 3]

class PlayerAI(BaseAI):
    H=[[65536,32768,16384,8192],[512,1024,2048,4096],[256,128,64,32],[2,4,8,16]]
    def getMove(self, stage):
        self.initialStage=stage
        self.ALPHA=-999999999  # alpha 的初始值 负的
        self.BETA=999999999  # beta的初始值 正的
        self.deep=0  # 遍历的时候的深浅
        move = self.SELECT()  # 转到select函数
        return move  # 返回的是我们需要的东西（数字）

    def SELECT(self):
        maxV = -999999999
        selectedMove=None
        nextStage=None
        for move in self.initialStage.getAvailableMoves():
            nextStage = self.initialStage.clone()
            nextStage.move(move)
            value = self.MIN(nextStage)
            if maxV < value:
                maxV=value 
                selectedMove=move
        return selectedMove

    def MAX(self, stage):
        self.deep=self.deep+1
        moves=stage.getAvailableMoves()
        nextStage=None
        if not moves or self.deep>6:
            self.deep=self.deep-1
            return self.Calculate(stage)
        average=-999999999
        for move in moves:  # 什么是moves
            nextStage=stage.clone()
            nextStage.move(move)  # move(move)

            average = max(average, self.MIN(nextStage))
           # average=max(average,self.MIN(nextStage, a, b))  # value = max(value, minValue(successor, a, b, depth + 1)) 中间括号里的是前面的nextstage
            #a = max(average, a)
            self.ALPHA = max(self.ALPHA, average)  # a = max(a, value)

            if(self.ALPHA >= self.BETA):

                return average

        return average

    def MIN(self, stage):
        self.deep=self.deep+1
        moves=stage.getAvailableCells()
        nextStage=None
        if not moves or self.deep>6:  # 可以说是他要往后看6步，到了6步之后就到了叶子节点可以计算估值，用calculate函数算
            self.deep=self.deep-1  # 不会再算了
            return self.Calculate(stage)
        average = 999999999  # a = 正无穷

        for move in moves:
            for value in range(2,5,2):
                nextStage=stage.clone()
                nextStage.setCellValue(move,value)
                nextV=self.MAX(nextStage)

                average=min(average,nextV)  # α := min(α, minimax(child, depth-1))  b = min(b, value)
                self.BETA = min(average, self.BETA)

                if (self.BETA <= self. ALPHA):
                    return average



        return average


    def Calculate(self, stage):
        sum = []
        for i in range(4):
            A = stage.map[i]
            B = sorted(A)
            result = (B == A or B == A[::-1])
            sum.append(result)
        for j in range(4):
            array = np.array(stage.map)
            B = array[:, j]
            b = list(B)
            C = sorted(b)
            result2 = (C == b or C == b[::-1])
            sum.append(result2)

        mono = 0
        for k in range(len(sum)):
            if sum[k] == True:
                mono = mono + 1

        em = stage.getAvailableCells()
        empty = len(em)

        diff = 0
        for i in range(3):
            for j in range(4):
                diff = diff + abs(stage.map[i + 1][j] - stage.map[i][j])

        for j in range(3):
            for i in range(4):
                diff = diff + abs(stage.map[i][j] - stage.map[i][j + 1])

        max = stage.getMaxTile()


        return mono + empty - diff * 0.0005 + max * 0.0001
