from msgdev import *

if __name__=='__main__':
    dev = MsgDevice()
    dev.open()
    # dev.sub_connect('tcp://192.168.1.80:55010')  # 下载端口
    dev.sub_connect('tcp://192.168.0.101:55010')
    dev.pub_bind('tcp://0.0.0.0:55002')  # 上传端口
    dev.sub_add_url('pro.left.speed')
    dev.sub_add_url('pro.right.speed')
    t = PeriodTimer(0.1)
    t.start()
    print('转发开始')
    while True:
        try:
            with t:
                left = dev.sub_get1('pro.left.speed')
                right = dev.sub_get1('pro.right.speed')
                dev.pub_set1('pro.left.speed', left)
                dev.pub_set1('pro.right.speed', right)
                print('上传 left: %04.4f, right: %04.4f'%(left, right))
        except KeyboardInterrupt as e:
            print('转发结束')
            break
