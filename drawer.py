import csv
import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec



class Drawer():
    def __init__(self):
        pass

    def drawFromData(self, data, name, cost=None, points=None):
        self.draw(data, name, cost, points)

    def drawFromFile(self, name):
        name = './data/' + name
        data = self.readOneCsvFile(name)
        data = [[eval(j) for j in i] for i in data]
        x = data[:-2]
        cost = data[-2]
        points = data[-1][0]
        self.draw(x, name, cost, points)

    def draw(self, data, name, cost=None, points=None):
        fig = plt.figure(figsize=(17, 8))
        fig.suptitle(name+'\n Cost: '+str(cost))
        gs = GridSpec(3, 2)

        # if cost:
        #     fig.text(0,0.90,'Cost: '+str(cost))

        axxy = fig.add_subplot(gs[:, 0])
        axuv = fig.add_subplot(gs[0, 1])
        axpo = fig.add_subplot(gs[1, 1])
        axlr = fig.add_subplot(gs[2, 1])

        x = [p[0] for p in points]
        y = [p[1] for p in points]

        axxy.plot(y, x, 'r--')

        axxy.set_aspect(1)
        axxy.set_ylim(min(x)-20, max(x)+20)
        axxy.set_xlim(min(y)-20, max(y)+20)

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
        print('saving ', name, '@', name + '.png')
        plt.show()
        fig.clear()

    def readOneCsvFile(self, file_name):
        with open(file_name) as f:
            r = csv.reader(f)
            re = [i for i in r]
        return re

import time
if __name__=='__main__':

    file_name = input('请输入文件名')

    # file_name = './fig/' + time.strftime("%Y-%m-%d__%H:%M", time.localtime())
    drawer = Drawer()
    drawer.drawFromFile(file_name)
