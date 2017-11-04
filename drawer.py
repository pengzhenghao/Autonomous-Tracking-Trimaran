import csv
import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec



class Drawer():
    def __init__(self):
        pass

    def drawFromData(self, data, name):
        self.draw(data, name)

    def drawFromFile(self, name):
        data = self.readOneCsvFile(name + '.csv')
        self.draw(data, name)

    def draw(self, data, name):
        fig = plt.figure(figsize=(17, 8))
        fig.suptitle(name)
        gs = GridSpec(3, 2)

        axxy = fig.add_subplot(gs[:, 0])
        axuv = fig.add_subplot(gs[0, 1])
        axpo = fig.add_subplot(gs[1, 1])
        axlr = fig.add_subplot(gs[2, 1])

        axxy.plot([0,0,50,50,0], [0, 50, 50, 0, 0], 'r--')

        axxy.set_aspect(1)
        axxy.set_ylim(-20, 70)
        axxy.set_xlim(-20, 70)

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
