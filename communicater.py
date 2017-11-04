import csv
import math
import time

from msgdev import MsgDevice, PeriodTimer


class Communicater(object):
    def __init__(self):
        self.dev = MsgDevice()
        self.dev.open()
        self.dev.sub_connect('tcp://192.168.1.150:55003')  # 下载端口
        self.dev.pub_bind('tcp://0.0.0.0:55002')  # 上传端口
        self.dev.sub_add_url('')

        self.dev_gnss = MsgDevice()
        self.dev_gnss.open()
        self.dev_gnss.sub_connect('tcp://192.168.1.150:55004')

        self.dev_ahrs = MsgDevice()
        self.dev_ahrs.open()
        self.dev_ahrs.sub_connect('tcp://192.168.1.150:55005')

        self.dev_volt = MsgDevice()
        self.dev_volt.open()
        self.dev_volt.sub_connect('tcp://192.168.1.150:55006')

        self.data_down = []
        self.data_up = [None, None]
        self.file_name = './data/'+time.strftime("%Y-%m-%d__%H:%M", time.localtime())
        self.f = open( self.file_name + '.csv', 'w')
        self.writer = csv.writer(self.f)

        self.dev_gnss.sub_add_url('gps.posx'),
        self.dev_gnss.sub_add_url('gps.posy'),
        self.dev_gnss.sub_add_url('gps.posz'),
        self.dev_gnss.sub_add_url('gps.hspeed'),
        self.dev_gnss.sub_add_url('gps.vspeed'),
        self.dev_gnss.sub_add_url('gps.track')

        self.dev_ahrs.sub_add_url('ahrs.yaw'),
        self.dev_ahrs.sub_add_url('ahrs.yaw_speed'),
        self.dev_ahrs.sub_add_url('ahrs.acce_x'),
        self.dev_ahrs.sub_add_url('ahrs.acce_y'),
        self.dev_ahrs.sub_add_url('ahrs.acce_z'),

        self.dev.sub_add_url('left.Motor_SpeedCalc')
        self.dev.sub_add_url('right.Motor_SpeedCalc')
        self.dev_volt.sub_add_url('voltage')

    def download(self):
        gps = [
            self.dev_gnss.sub_get1('gps.posx'),
            self.dev_gnss.sub_get1('gps.posy'),
            self.dev_gnss.sub_get1('gps.posz'),
            self.dev_gnss.sub_get1('gps.hspeed'),
            self.dev_gnss.sub_get1('gps.vspeed'),
            self.dev_gnss.sub_get1('gps.track')
        ]

        ahrs = [
            self.dev_ahrs.sub_get1('ahrs.yaw'),
            self.dev_ahrs.sub_get1('ahrs.yaw_speed'),
            self.dev_ahrs.sub_get1('ahrs.acce_x'),
            self.dev_ahrs.sub_get1('ahrs.acce_y'),
            self.dev_ahrs.sub_get1('ahrs.acce_z'),
        ]

        l_m = self.dev.sub_get1('left.Motor_SpeedCalc')
        r_m = self.dev.sub_get1('right.Motor_SpeedCalc')
        volt = self.dev_volt.sub_get1('voltage')
        return gps, ahrs, l_m, r_m, volt

    def getNEData(self):
        """
        :return:  x,y,u,v,yaw,omega in NE sys.
        """
        gps, ahrs, l_m, r_m, volt = self.download()
        yaw = ahrs[0] - 5 * math.pi / 180
        U = gps[3] * math.cos(gps[5])  # 北东系速度
        V = gps[3] * math.sin(gps[5])
        self.data_down = [gps[0], gps[1], U, V, yaw, ahrs[1]]
        return {'x': gps[0], 'y': gps[1], 'u': U, 'v': V, 'phi': yaw, 'alpha': ahrs[1]}

    def upload(self, left, right):
        self.dev.pub_set1('pro.left.sp1eed', left)
        self.dev.pub_set1('pro.right.speed', right)
        self.data_up = [left, right]
        print('uploaded', left, right)

    def record(self):
        self.writer.writerow(self.data_down + self.data_up)
        print('Saved: ', self.data_down + self.data_up)

    def __del__(self):
        self.dev.close()
        self.f.close()


if __name__ == "__main__":
    lis = []
    c = Communicater()
    t = PeriodTimer(0.1)
    t.start()
    while True:
        try:
            with t:
                c.getNEData()
                # c.upload(0, 0)
                c.record()
        except KeyboardInterrupt as e:
            c.__del__()
            break

    print('Test ended!')
