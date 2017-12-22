# MsgDev库使用说明(pengzh, 2017.10)


        #Connect to control program
        dev_pro = MsgDevice()		#1
        dev_pro.open()
        dev_pro.sub_connect('tcp://127.0.0.1:55002')
        dev_pro.pub_bind('tcp://0.0.0.0:55003')

第一行创造实例
第二行开启收发器
第三行设置【接收通道】
第四行设置【发送通道】


        # Connect to joystick
        dev_joy = MsgDevice()		#1
        dev_joy.open()
        dev_joy.sub_connect('tcp://127.0.0.1:55001')
        dev_joy.sub_add_url('js.autoctrl')

第三行设置【接收通道】，第四行把那个url地址起个名字【autoctrl】


        left_motor = Motor(dev_pro, dev_joy,'left', 0x01, master)
        right_motor = Motor(dev_pro,dev_joy,'right', 0x02, master)

两个张磊学长写的Motor类，第一个参数为发送器，第二个参数为接收器，别的不知道


        while True:
            with t:
                autoctrl = dev_joy.sub_get1('js.autoctrl')	#1
                dev_pro.pub_set1('autoctrl', autoctrl)
                left_motor.update(autoctrl)
                right_motor.update(autoctrl)

程序主循环，第一行把【接收器dev_joy】收到的数据存在【autoctrl】。
第二行用【发送器dev_pro】把数据发射到之前存出国的【autoctrl】地址处，程序会自动查找名字叫【autoctrl】的一条ip地址，然后发过去。
第三四行是学长写的motor的一些功能。