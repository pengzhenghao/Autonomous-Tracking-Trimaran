import time

from PID import PID
from communicater import Communicater
from decisionMaker import Maker
# from drawer import Drawer
from msgdev import PeriodTimer

kp = 800
ki = 3
kd = 10

points = [
    [-42, 46],
    [-17, -34],
    [-85, -24],
    [-85, 46],
    [-42, 46]
]

if __name__ == '__main__':
    c = Communicater()
    pid = PID(kp=kp, ki=ki, kd=kd, minout=-2500, maxout=500, sampleTime=0.1)
    timer = PeriodTimer(0.1)

    maker = Maker(points)
    cost = 0
    data = []
    i = 0

    while True:
        try:
            with timer:
                state = c.getNEData()
                ideal_angle = maker.getDecision(state)
                cost += maker.getCost(state)
                if ideal_angle == -1000:
                    c.upload(0, 0)
                    print('试验成功！')
                    break
                output = pid.compute(state['phi'], ideal_angle)
                output = 0 if abs(output) < 5 else output
                left, right = -1000 - output, 1000
                c.upload(left, right)
                data.append([state['x'], state['y'], state['u'], state['v'], state['phi'], state['alpha'], left, right])
                c.record()
                i += 1
        except KeyboardInterrupt as e:
            c.writer.writerow([cost])
            c.writer.writerow([points])
            c.__del__()
            break

    print('Gross Cost: ', cost, 'Average Cost:', cost / (i+1e-5))
