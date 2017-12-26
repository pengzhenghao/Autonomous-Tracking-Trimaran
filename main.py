import time

from PID import PID
from communicater import Communicater
from decisionMaker import Maker
from drawer import Drawer
from msgdev import PeriodTimer
import numpy as np
import threading
kp = 1200
ki = 3
kd = 10

LOG_RADIUS = 6
REACH_RADIUS = 4
initial_points = [0.14296570229, 15.875725953]


ideal_points = [
    [-30, -15],
    [-80, -17],
    [-80, 40],
    [-30, 40],
    [-30, -15]
]



star = [
    [-20, 10],
    [-70, -8],
    [-35, 40],
    [-35, -20],
    [-70, 28],
    [-20, 10]
]



if __name__ == '__main__':
    c = Communicater()
    pid = PID(kp=kp, ki=ki, kd=kd, minout=-2000, maxout=2000, sampleTime=0.1)
    timer = PeriodTimer(0.1)
    target = star
    points = [[p[0] - initial_points[0], p[1] - initial_points[1]] for p in target]

    maker = Maker(points, REACH_RADIUS)
    cost = []
    data = []
    i = 0
    drawer = Drawer()

    decay_factor = 1

    t = threading.Thread(target=drawer.thread, args=(points,maker.getCost))
    t.setDaemon(True)
    t.start()
    while True:
        try:
            with timer:
                state = c.getNEData()
                ideal_angle, decay_factor = maker.wrapper_LOG(state, radius=LOG_RADIUS, decay_radius=0)
                cost.append(maker.getCost(state))
                if ideal_angle == -1000:
                    c.upload(0, 0)  # 保护措施
                    print('试验成功！')
                    break

                output = pid.compute(state['phi'], ideal_angle)
                output = 0 if abs(output) < 5 else output

                baseline = 1000 * decay_factor
                left, right = baseline + output / 2, baseline - output / 2
                left = max(min(left, 2000), -2000)
                right = max(min(right, 2000), -2000)

                c.upload(-left, right)
                adata = [state['x'], state['y'], state['u'], state['v'], state['phi'], state['alpha'], state['lm'], state['rm']]
                data.append(adata)
                c.record()
                i += 1


        except KeyboardInterrupt as e:
            c.upload(0, 0)  # 保护措施
            c.__del__()
            break

    print(i)
    print('Gross Cost: ', np.sum(cost), 'Average Cost:', np.mean(cost))
    file_name = c.file_name
    drawer.drawFromData(data, file_name, np.mean(cost), points)
