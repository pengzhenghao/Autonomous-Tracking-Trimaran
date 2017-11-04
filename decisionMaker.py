import math
from math import pi


RADIUS = 2



class Maker:
    def __init__(self, points):
        self.points = points
        self.s = points[0]
        self.e = points[1]
        self.pointer = 1


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

        # m = ((y1 * y + x1 * x - y0 * y - x0 * x) * (x1 - x0) + (
        #     x1 * y0 - x0 * y1) * (y1 - y0)) / (
        #         (y1 - y0) * (y1 - y0) + (x1 - x0) * (x1 - x0))
        # n = ((y1 * y + x1 * x - y0 * y - x0 * x) * (y1 - y0) - (
        #     x1 * y0 - x0 * y1) * (x1 - x0)) / (
        #         (y1 - y0) * (y1 - y0) + (x1 - x0) * (x1 - x0))
        # mid_point_x = (m + x1) / 2
        # mid_point_y = (n + y1) / 2

        mid_point_x = x1
        mid_point_y = y1

        direction = math.atan((mid_point_y - y) / (mid_point_x - x))




        dx = mid_point_x - x
        dy = mid_point_y - y

        if dx<0:
            direction = pi + direction
        elif dy<0:
            direction = 2 * pi + direction



        if ((x1-x)**2 + (y1-y)**2) < RADIUS**2:
            if self.pointer == (len(self.points) - 1):
                return -1000
            self.s = self.points[self.pointer]
            self.e = self.points[self.pointer+1]
            self.pointer += 1
        return direction



