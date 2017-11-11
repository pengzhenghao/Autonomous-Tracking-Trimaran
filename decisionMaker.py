import math
from math import pi

RADIUS = 4


class Maker:
    def __init__(self, points):
        self.points = points
        self.s = points[0]
        self.e = points[1]
        self.pointer = 0

    def getCost(self, state):
        x, y = state['x'], state['y']
        a, b = self._calculateFootPoint(x, y)
        return (a - x) ** 2 + (b - y) ** 2

    def getDecision(self, state):
        # 请在这里输入你的循迹算法, state是一个字典, 共有6个量
        # 可以使用字符串调取, 'x', 'y', 'u','v','phi','alpha'
        # 如:
        # x = state['x']
        # 请返回理想航向角, 弧度制, 范围0~2PI

        x = state['x']
        y = state['y']

        x0, y0 = self.s
        x1, y1 = self.e

        if self.pointer==0:
            if ((x0 - x) ** 2 + (y0 - y) ** 2) < RADIUS ** 2:
                self.pointer += 1
            return math.atan2(y1 - y, x1 - x)

        if ((x1 - x) ** 2 + (y1 - y) ** 2) < RADIUS ** 2:
            if self.pointer == (len(self.points) - 1):
                return -1000
            self._updateStartAndEndPoint()

        a, b = self._calculateFootPoint(x, y)

        mid_point_x = (x1 + 5*a) / 6
        mid_point_y = (y1 + 5*b) / 6

        direction = math.atan2(mid_point_y - y, mid_point_x - x)

        return direction

    def _updateStartAndEndPoint(self):
        self.s = self.points[self.pointer]
        self.e = self.points[self.pointer + 1]
        self.pointer += 1

    def _calculateFootPoint(self, x, y):
        x0, y0 = self.s
        x1, y1 = self.e
        p = x1 - x0
        q = y1 - y0
        a = (x * (p ** 2) + y * p * q - y0 * p * q + (q ** 2) * x0) / (p ** 2 + q ** 2)
        b = (x * p * q + y * (q ** 2) + (p ** 2) * y0 - p * q * x0) / (p ** 2 + q ** 2)
        return a, b