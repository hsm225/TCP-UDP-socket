# -*- coding:utf-8 -*-
__author__ = 'Administrator'

import socket, time, Tkinter, sys, ctypes, inspect, threading

class Udp_Client_Function(object):
    def __init__(self):
        #self.signal，用于区别“侦听”或“停止”
        self.signal = 0
        #用于统计发送给客户端的数据条数
        self.send_num = 0
        #用于统计接收客户端发送数据的条数
        self.recv_num = 0
        #用于将客户端的ip+port和socket套件组合成字典的形式，便于查找
        self.client_list = {}
        #用于将客户端的ip+port设置为列表
        self.client_addr_list = []
        #用于将客户端的socket套件设置为列表，后面这三条一般都在一起使用
        self.client_conn_list = []
        #下面三个参数用于统计定时发送的条数
        self.send_num_1 = 0
        self.send_num_2 = 0
        self.send_num_3 = 0

    def log_recode(self, log_checkbutton):
        '日志记录函数，用于将收发的日志写入文件里面；以服务器IP+端口作为文件名'
        if log_checkbutton.get():
            try:
                self.f = open("%s_%s_udp_client.txt" % (self.HOST, self.PORT), 'ab')
            except Exception, e:
                print u'记录日志失败，请重新勾选！'
                self.f.close()
        else:
            try:
                self.f.close()
            except Exception, e:
                print e

    def clear_data_text(self, data_daxt, send_num_entry, receive_num_entry):
        '对应udp_client面板>统计框架>清空按钮的函数，用于清空接收和发送的数据，全部置为0'
        data_daxt.delete(0, data_daxt.size())
        self.send_num = 0
        send_num_entry.set(self.send_num)
        self.recv_num = 0
        receive_num_entry.set(self.recv_num)

    def send_data(self, send_entry_data, send_num_entry, data_text):
        '对应udp_client面板>发送数据框架>发送按钮的函数，用于向客户端发送带条数据'
        self.s.sendto(send_entry_data, (self.HOST, self.PORT))
        self.signal = 1
        # 服务器发送给客户端的数据，同样显示在接收数据的框架里面
        data_text.insert(Tkinter.END, "%s [%s>>server] %d: %s\n" % (time.strftime("%H:%M:%S"), self.s.getsockname(), len(send_entry_data),  send_entry_data))
        # 如果开启了日志功能，那么将发送给客户端的数据记录日志
        try:
            self.f.write("%s [%s>>server] %d: %s\n" % (time.strftime("%H:%M:%S"), self.s.getsockname(), len(send_entry_data),  send_entry_data))
        except Exception, e:
            print e
        self.send_num += 1
        send_num_entry.set(self.send_num)

    def sent_data_timing_circulation_1(self, send_frame_button, send_entry_data, send_interval, send_num_entry, data_text):
        'sent_data_timing_circulation_1，就是定时发送1函数拉起的线程对应的函数，用于循环形式发送数据'
        # 如果在这个线程里面不需要改变aa的值，那下面的global aa就不需要，同时aa不能在这里进行更改；
        # 在这里将aa置为全局变量，那么就可以在这里对aa进行赋值。
        global aa
        data_text.insert(Tkinter.END, "%s [%s>>server] %d: （定时发送1开始）%s\n" % (time.strftime("%H:%M:%S"), self.s.getsockname(), len(send_entry_data),  send_entry_data))
        sleep_time = float(send_interval.get())/1000
        send_entry_data_all = ''
        wait_time = 0.0
        self.signal = 1
        while aa and self.connect_signal:
            #下面的try，只要是用于当获取选中客户端失败、发送数据失败、插入数据到显示区域失败时；可以将定时按钮重置；同时可以再次定时发送
            try:
                while wait_time < 0.2 and len(send_entry_data_all) < 1400:
                    send_entry_data_all += send_entry_data
                    wait_time += sleep_time
                    self.send_num += 1
                    self.send_num_1 += 1
                    time.sleep(sleep_time)
                self.s.sendto(send_entry_data_all, (self.HOST, self.PORT))
                send_num_entry.set(self.send_num)
                wait_time = 0.0
                send_entry_data_all = ''
            except Exception, e:
                data_text.insert(Tkinter.END, "%s [%s>>server] %d: （定时发送1结束, 发送次数%d）%s\n" % (time.strftime("%H:%M:%S"), self.s.getsockname(), len(send_entry_data), self.send_num_1, send_entry_data))
                self.send_num_1 = 0
                send_frame_button.set(u'定时发送')

    def send_data_timing_1(self, send_frame_button, send_entry_data, send_interval, send_num_entry, data_text):
        '对应udp_client面板>发送数据大框架>发送数据小框架1>定时发送按钮的函数，用于向客户端定时发送数据'
        # 这个全局变量aa仅用于发送数据小框架1的定时发送，使用aa来对是否进行定时发送进行判断；aa作用于send_data_timing_1函数和
        # 由send_data_timing_1函数拉起的线程。
        # 点击“定时发送”>aa=1>拉起线程sent_data_timing_circulation_1>循环发送数据”
        # 点击“暂停”>因为这个时候“定时发送”按钮的值为“暂停”，也就是要暂停定时发送>aa=0>因为aa为全局变量，所以send_data_timing_circulation_1
        # 线程的aa同样也变成了0，while循环就用中断，定时发送就终止。
        global  aa
        try:
            if send_frame_button.get() == u'定时发送' and self.signal:
                aa = 1
                if send_interval.get().isdigit():
                    send_data_timing_thread = threading.Thread(target=self.sent_data_timing_circulation_1, args=(send_frame_button, send_entry_data, send_interval,  send_num_entry, data_text))
                    send_data_timing_thread.start()
                    send_frame_button.set(u'暂停')
                else:
                    print u"请输入正整数"
            else:
                data_text.insert(Tkinter.END, "%s [%s>>server] %d: （定时发送1结束, 发送次数%d）%s\n" % (time.strftime("%H:%M:%S"), self.s.getsockname(), len(send_entry_data), self.send_num_1, send_entry_data))
                self.send_num_1 = 0
                send_frame_button.set(u'定时发送')
                aa =0
        except Exception, e:
            send_frame_button.set(u'定时发送')

    def sent_data_timing_circulation_2(self, send_frame_button, send_entry_data, send_interval, send_num_entry, data_text):
        'sent_data_timing_circulation_2，就是定时发送1函数拉起的线程对应的函数，用于循环形式发送数据'
        # 如果在这个线程里面不需要改变bb的值，那下面的global bb就不需要，同时bb不能在这里进行更改；
        # 在这里将bb置为全局变量，那么就可以在这里对bb进行赋值。
        global bb
        data_text.insert(Tkinter.END, "%s [%s>>server] %d: （定时发送2开始）%s\n" % (time.strftime("%H:%M:%S"), self.s.getsockname(), len(send_entry_data),  send_entry_data))
        sleep_time = float(send_interval.get())/1000
        send_entry_data_all = ''
        wait_time = 0.0
        self.signal = 1
        while bb and self.connect_signal:
            #下面的try，只要是用于当获取选中客户端失败、发送数据失败、插入数据到显示区域失败时；可以将定时按钮重置；同时可以再次定时发送
            try:
                while wait_time < 0.2 and len(send_entry_data_all) < 1400:
                    send_entry_data_all += send_entry_data
                    wait_time += sleep_time
                    self.send_num += 1
                    self.send_num_2 += 1
                    time.sleep(sleep_time)
                self.s.sendto(send_entry_data_all, (self.HOST, self.PORT))
                send_num_entry.set(self.send_num)
                wait_time = 0.0
                send_entry_data_all = ''
            except Exception, e:
                data_text.insert(Tkinter.END, "%s [%s>>server] %d: （定时发送2结束, 发送次数%d）%s\n" % (time.strftime("%H:%M:%S"), self.s.getsockname(), len(send_entry_data), self.send_num_2, send_entry_data))
                self.send_num_1 = 0
                send_frame_button.set(u'定时发送')

    def send_data_timing_2(self, send_frame_button, send_entry_data, send_interval, send_num_entry, data_text):
        '对应udp_client面板>发送数据大框架>发送数据小框架1>定时发送按钮的函数，用于向客户端定时发送数据'
        # 这个全局变量bb仅用于发送数据小框架1的定时发送，使用bb来对是否进行定时发送进行判断；bb作用于send_data_timing_2函数和
        # 由send_data_timing_2函数拉起的线程。
        # 点击“定时发送”>bb=2>拉起线程sent_data_timing_circulation_2>循环发送数据”
        # 点击“暂停”>因为这个时候“定时发送”按钮的值为“暂停”，也就是要暂停定时发送>bb=0>因为bb为全局变量，所以send_data_timing_circulation_2
        # 线程的bb同样也变成了0，while循环就用中断，定时发送就终止。
        global  bb
        try:
            if send_frame_button.get() == u'定时发送' and self.signal:
                bb = 1
                if send_interval.get().isdigit():
                    send_data_timing_thread = threading.Thread(target=self.sent_data_timing_circulation_2, args=(send_frame_button, send_entry_data, send_interval,  send_num_entry, data_text))
                    send_data_timing_thread.start()
                    send_frame_button.set(u'暂停')
                else:
                    print u"请输入正整数"
            else:
                data_text.insert(Tkinter.END, "%s [%s>>server] %d: （定时发送2结束, 发送次数%d）%s\n" % (time.strftime("%H:%M:%S"), self.s.getsockname(), len(send_entry_data), self.send_num_2, send_entry_data))
                self.send_num_2 = 0
                send_frame_button.set(u'定时发送')
                bb =0
        except Exception, e:
            send_frame_button.set(u'定时发送')

    def sent_data_timing_circulation_3(self, send_frame_button, send_entry_data, send_interval, send_num_entry, data_text):
        'sent_data_timing_circulation_3，就是定时发送1函数拉起的线程对应的函数，用于循环形式发送数据'
        # 如果在这个线程里面不需要改变cc的值，那下面的global cc就不需要，同时cc不能在这里进行更改；
        # 在这里将cc置为全局变量，那么就可以在这里对cc进行赋值。
        global cc
        data_text.insert(Tkinter.END, "%s [%s>>server] %d: （定时发送3开始）%s\n" % (time.strftime("%H:%M:%S"), self.s.getsockname(), len(send_entry_data),  send_entry_data))
        sleep_time = float(send_interval.get())/1000
        send_entry_data_all = ''
        wait_time = 0.0
        self.signal = 1
        while cc and self.connect_signal:
            #下面的try，只要是用于当获取选中客户端失败、发送数据失败、插入数据到显示区域失败时；可以将定时按钮重置；同时可以再次定时发送
            try:
                while wait_time < 0.2 and len(send_entry_data_all) < 1400:
                    send_entry_data_all += send_entry_data
                    wait_time += sleep_time
                    self.send_num += 1
                    self.send_num_3 += 1
                    time.sleep(sleep_time)
                self.s.sendto(send_entry_data_all, (self.HOST, self.PORT))
                send_num_entry.set(self.send_num)
                wait_time = 0.0
                send_entry_data_all = ''
            except Exception, e:
                data_text.insert(Tkinter.END, "%s [%s>>server] %d: （定时发送3结束, 发送次数%d）%s\n" % (time.strftime("%H:%M:%S"), self.s.getsockname(), len(send_entry_data), self.send_num_3, send_entry_data))
                self.send_num_3 = 0
                send_frame_button.set(u'定时发送')

    def send_data_timing_3(self, send_frame_button, send_entry_data, send_interval, send_num_entry, data_text):
        '对应udp_client面板>发送数据大框架>发送数据小框架3>定时发送按钮的函数，用于向客户端定时发送数据'
        # 这个全局变量cc仅用于发送数据小框架3的定时发送，使用cc来对是否进行定时发送进行判断；cc作用于send_data_timing_3函数和
        # 由send_data_timing_3函数拉起的线程。
        # 点击“定时发送”>cc=1>拉起线程sent_data_timing_circulation_3>循环发送数据”
        # 点击“暂停”>因为这个时候“定时发送”按钮的值为“暂停”，也就是要暂停定时发送>cc=0>因为aa为全局变量，所以send_data_timing_circulation_3
        # 线程的cc同样也变成了0，while循环就用中断，定时发送就终止。
        global  cc
        try:
            if send_frame_button.get() == u'定时发送' and self.signal:
                cc = 1
                if send_interval.get().isdigit():
                    send_data_timing_thread = threading.Thread(target=self.sent_data_timing_circulation_3, args=(send_frame_button, send_entry_data, send_interval,  send_num_entry, data_text))
                    send_data_timing_thread.start()
                    send_frame_button.set(u'暂停')
                else:
                    print u"请输入正整数"
            else:
                data_text.insert(Tkinter.END, "%s [%s>>server] %d: （定时发送3结束, 发送次数%d）%s\n" % (time.strftime("%H:%M:%S"), self.s.getsockname(), len(send_entry_data), self.send_num_3, send_entry_data))
                self.send_num_3 = 0
                send_frame_button.set(u'定时发送')
                cc =0
        except Exception, e:
            send_frame_button.set(u'定时发送')

    def signal_judge(self, param_list):
        '由Connect函数拉起的线程对应的函数，用于处于数据的接收，并插入到数据区显示'
        while not self.signal:
            pass
        self.receive_data_thread = threading.Thread(target=self.receive_data, args=(param_list, ))
        self.receive_data_thread.start()

    def receive_data(self, param_list):
        while self.connect_signal:
            data, addr = self.s.recvfrom(1024)
            print addr
            if data != '':
                param_list[0].insert(Tkinter.END, "%s [server>>%s] %d: %s\n" % (time.strftime("%H:%M:%S"), self.s.getsockname(), len(data),  data))
                try:
                    self.f.write("%s [server>>%s] %d: %s\n" % (time.strftime("%H:%M:%S"), self.s.getsockname(), len(data),  data))
                except Exception, e:
                    print e
                #接收到一个数据，数据统计+1，并显示
                self.recv_num += 1
                param_list[2].set(self.recv_num)
                #当接收到的数据超过了1024的时候，就将接收数据分区里面的第一行删除（也就是最早接收到的行）
                if self.recv_num > 1024:
                    param_list[0].delete(0)
            # 走到这个else，说明是客户端主动断开了连接，服务器这边也要有相应的处理，该删除的删除，该记录的记录
            else:
                self.s.close()
                param_list[11].set(u"连接")
                try:
                    self.f.close()
                except Exception, e:
                    pass

    def end_thread(self):
        # end_thread，该函数也非常有用；当侦听按钮从“停止”变“侦听”的时候，也就是服务器不再侦听时，由它来进行收尾工作
        self.signal = 0
        self.connect_signal =0

    def Connect(self, param_list):
        '对应udp_client面板>侦听框架>侦听按钮的函数，用于udp_client的侦听；param_list就是从侦听按钮附带下来的参数的列表'
        # 这个s就是后面的socket，这里将其设置为全局变量，主要是用于出现异常时的处理
        global s
        if param_list[11].get() == u'连接':
            try:
                # self.signal，对应侦听与否，当self.signal=0的时候，所有的连接等删除重置
                self.connect_signal = 1
                self.HOST = param_list[9].get()
                self.PORT = int(param_list[10].get())
                #self.HOST = '192.168.150.1'
                #self.PORT = 20000
                self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                print 'open:',self.s._sock
                # 这里采用线程方式拉起接受函数，如果不使用线程，那么会因为还没有连接到服务器，没有产生本端的端口而无法接受，导致程序无法走下去。
                self.accept_thread = threading.Thread(target=self.signal_judge, args=(param_list, ))
                # thread.sedDaemon(True)，作用是将该thread设置父线程，当父线程被回收时，其下面的子线程都需要被回收。
                self.accept_thread.setDaemon(True)
                self.accept_thread.start()
                param_list[11].set(u'断开')
            except Exception, e:
                print e
        else:
            # 当点击“停止”按钮，所有的参数都重置
            self.connect_signal = 0
            param_list[11].set(u'连接')
            param_list[13].set(u"定时发送")
            param_list[14].set(u"定时发送")
            param_list[15].set(u"定时发送")
            self.end_thread()
            try:
                self.f.close()
            except:
                pass
            param_list[12].set(0)
            self.s.close()

'''
0:self.data_text
1:self.send_num
2:self.receive_num
3:self.send_frame_entry_1
4:self.send_timing_frame_entry_1
5:self.send_frame_label_2
6:self.send_timing_frame_entry_2
7:self.send_frame_entry_3
8:self.send_timing_frame_entry_3
9:self.ipaddr_server_entry
10:self.port_server_entry
11:self.connect_v
12:self.log_checkbutton_v
13:self.listen_v_send_timing_1
14:self.listen_v_send_timing_2
15:self.listen_v_send_timing_3
'''