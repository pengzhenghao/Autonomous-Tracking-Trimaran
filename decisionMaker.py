import math
from math import pi


class Maker:
    def __init__(self, points, radius=3):
        self.points = points
        self.s = points[0]
        self.e = points[1]
        self.pointer = 0
        self.RADIUS = radius


    def wrapper_LOG(self, state, radius, decay_radius):
        direction = self.LOGMaker(state, radius)
        x, y = state['x'], state['y']

        if self.pointer != 0:
            dis = (self.e[0] - x ) ** 2 + (self.e[1] - y ) ** 2
            dis_s = (self.s[0] - x ) ** 2 + (self.s[1] - y ) ** 2
            if dis < (decay_radius ** 2):
                return direction, math.sqrt(dis)/decay_radius
            if dis_s < (decay_radius ** 2):
                return direction, math.sqrt(dis_s)/decay_radius
        return direction, 1

    def wrapper_divide(self, state, decay_radius):
        direction = self.getDecision(state)
        x, y = state['x'], state['y']
        if self.pointer != 0:
            dis = (self.e[0] - x ) ** 2 + (self.e[1] - y ) ** 2
            if dis < decay_radius ** 2:
                print('now dis', dis)
                # return direction, 1 - math.exp(-math.sqrt(dis))
                return direction, math.sqrt(dis)/decay_radius
        return direction, 1


    def getCost(self, state):
        if self.pointer==0:
            return 0
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
            return self._inintialDirection(x, y)

        if ((x1 - x) ** 2 + (y1 - y) ** 2) < self.RADIUS ** 2:
            if self.pointer == (len(self.points) - 1):
                return -1000
            self._updateStartAndEndPoint()

        a, b = self._calculateFootPoint(x, y)

        mid_point_x = (x1 + 5*a) / 6
        mid_point_y = (y1 + 5*b) / 6

        direction = math.atan2(mid_point_y - y, mid_point_x - x)

        return direction

    def LOGMaker(self, state, radius):
        x = state['x']
        y = state['y']

        if self.pointer==0:
            return self._inintialDirection(x, y)

        x0, y0 = self.s
        x1, y1 = self.e

        a, b = self._calculateFootPoint(x, y)

        distance = ((x - a) ** 2 + (y - b) ** 2) ** 0.5

        if distance >= radius:
            direction = math.atan2((b - y), (a - x))
            direction = direction + 2*pi if direction < 0 else direction
            return direction

        else:
            along_distance = (radius ** 2 - distance ** 2) ** 0.5
            angle = math.atan2((y1 - y0), (x1 - x0))

            m = a + along_distance * math.cos(angle)
            n = b + along_distance * math.sin(angle)

            direction = math.atan2((n - y), (m - x))
            direction = direction + 2*pi if direction < 0 else direction

            if ((x1 - x) ** 2 + (y1 - y) ** 2) < self.RADIUS ** 2:
                if self.pointer == (len(self.points) - 1):
                    return -1000
                self._updateStartAndEndPoint()
            return direction

    def _inintialDirection(self, x, y):
        x0, y0 = self.s
        x1, y1 = self.e
        if ((x0 - x) ** 2 + (y0 - y) ** 2) < (self.RADIUS+1) ** 2:
            self.pointer += 1
        direction = math.atan2(y0 - y, x0 - x)
        direction = direction + 2*pi if direction<0 else direction
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