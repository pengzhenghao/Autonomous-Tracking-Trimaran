import csv
from time import time as func_t

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec

from communicater import Communicater
from msgdev import PeriodTimer


class Drawer():
    def __init__(self, points=None):
        self.animating = False
        self.axxy, self.axuv, self.axpo, self.axlr, self.fig = [None] * 5
        self.lxy, self.lu, self.lv, self.lp, self.lo, self.ll, self.lr = [None] * 7
        self.data = []
        self.points = []
        self.c = Communicater(upload=False)

    def animation_initialize(self, points=None):
        if not points:
            assert self.points
            points = self.points
        self.i = 0
        self.animating = True
        self.fig = plt.figure(figsize=(17, 8))
        self.fig.show()
        self.fig.suptitle(u'正在实时绘图，已进行%04.1f秒' % 0)
        gs = GridSpec(3, 2)
        self.axxy = self.fig.add_subplot(gs[:, 0])
        self.axuv = self.fig.add_subplot(gs[0, 1])
        self.axpo = self.fig.add_subplot(gs[1, 1])
        self.axlr = self.fig.add_subplot(gs[2, 1])
        x = [p[0] for p in points]
        y = [p[1] for p in points]
        self.axxy.plot(y, x, 'r--')
        self.axxy.set_aspect(1)
        self.axxy.set_ylim(min(x) - 10, max(x) + 30)
        self.axxy.set_xlim(min(y) - 10, max(y) + 10)

        self.lxy = self.axxy.plot([], [])[0]
        self.lu = self.axuv.plot([], label='U')[0]
        self.lv = self.axuv.plot([], label='V')[0]
        self.axuv.legend(loc='lower left')

        self.lp = self.axpo.plot([], label=r'$\phi$')[0]
        self.lo = self.axpo.plot([], label=r'$\omega$')[0]
        self.axpo.legend(loc='lower left')

        self.ll = self.axlr.plot([], label='lp')[0]
        self.lr = self.axlr.plot([], label='rp')[0]
        self.axlr.legend(loc='lower left')
        self.starttime = func_t()

    def animate(self, adata, i, cost=0):
        assert self.animating == True
        i = i / 10
        time = func_t() - self.starttime
        self.fig.suptitle(u'正在实时散点绘图，已进行%04.1f秒\ncost:%.5f' % (time, cost))

        self.axxy.scatter(adata[1], adata[0], color='black', marker='.')

        self.axuv.scatter(i, adata[2], color='blue', marker='.')
        self.axuv.scatter(i, adata[3], color='green', marker='.')
        self.axuv.set_ylim(-1, 1)
        self.axuv.set_xlim(0, i + 10)

        self.axpo.scatter(i, adata[4], color='blue', marker='.')
        self.axpo.scatter(i, adata[5], color='green', marker='.')
        self.axpo.set_ylim(-0.2, 7)
        self.axpo.set_xlim(0, i + 10)

        self.axlr.scatter(i, adata[6], color='blue', marker='.')
        self.axlr.scatter(i, adata[7], color='green', marker='.')
        self.axlr.set_ylim(-1500, 1500)
        self.axlr.set_xlim(0, i + 10)

        self.fig.canvas.draw()
        return

    def drawFromData(self, data, name, cost, points):
        self.draw(data, name, cost, points)

    def drawFromFile(self, name, cost, points):
        name = './data/' + name
        data = self.readOneCsvFile(name)
        data = [[eval(j) for j in i] for i in data]
        self.draw(data, name, cost, points)

    def draw(self, data, name, cost=-1, points=None):
        fig = plt.figure(figsize=(17, 8))
        fig.suptitle(name + '\n Cost: ' + str(cost))
        gs = GridSpec(3, 2)

        axxy = fig.add_subplot(gs[:, 0])
        axuv = fig.add_subplot(gs[0, 1])
        axpo = fig.add_subplot(gs[1, 1])
        axlr = fig.add_subplot(gs[2, 1])

        if points == None:
            x = [0, 0, 50, 50, 0]
            y = [0, 50, 50, 0, 0]
        else:
            x = [p[0] for p in points]
            y = [p[1] for p in points]

        axxy.plot(y, x, 'r--')

        axxy.set_aspect(1)
        axxy.set_ylim(min(x) - 10, max(x) + 30)
        axxy.set_xlim(min(y) - 10, max(y) + 10)

        astate = np.array(data)
        astate = astate.transpose()

        axxy.plot(astate[1], astate[0])

        axuv.plot(astate[2], label='U')
        axuv.plot(astate[3], label='V')
        axuv.legend(loc='lower left')

        axpo.plot(astate[4], label=r'$\phi$')
        axpo.plot(astate[5], label=r'$\omega$')
        axpo.legend(loc='lower left')

        axlr.plot(astate[6], label='lp')
        axlr.plot(astate[7], label='rp')
        axlr.legend(loc='lower left')

        fig.savefig(name + '.png', dpi=200)
        print('saved ', name, '@', name + '.png')

    def readOneCsvFile(self, file_name):
        with open(file_name) as f:
            r = csv.reader(f)
            re = [i for i in r]
        return re

    def thread(self, points, costfunc):
        self.animation_initialize(points)
        timer = PeriodTimer(0.1)
        i = 0
        cost = []
        while True:
            try:
                with timer:
                    state = self.c.getNEData()
                    cost.append(costfunc(state))
                    adata = [state['x'], state['y'], state['u'], state['v'], state['phi'], state['alpha'], state['lm'],
                             state['rm']]
                    self.animate(adata, i, np.mean(cost))
                    i += 1
            except:
                print('Error happened in drawing!!!!')
                break

    def __del__(self):
        print('deleted')


d = Drawer()
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
target = star
points = [[p[0] - initial_points[0], p[1] - initial_points[1]] for p in target]

d.drawFromFile('1351.csv', 0.587098923957, points )