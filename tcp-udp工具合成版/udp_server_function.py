# -*- coding:utf-8 -*-
__author__ = 'Administrator'

import socket, time, Tkinter, sys, ctypes, inspect, threading

class Ucp_Server_Function(object):
    def __init__(self):
        #self.signal，用于区别“侦听”或“停止”
        self.signal = 1
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
        #下面的3个参数用于统计三个定时发送的条数
        self.send_num_1 = 0
        self.send_num_2 = 0
        self.send_num_3 = 0

    def log_recode(self, log_checkbutton):
        '日志记录函数，用于将收发的日志写入文件里面；以服务器IP+端口作为文件名'
        if log_checkbutton.get():
            try:
                self.f = open("%s_%s_udp_server.txt" % (self.HOST, self.PORT), 'ab')
            except Exception, e:
                print u'记录日志失败，请重新勾选！'
                self.f.close()
        else:
            try:
                self.f.close()
            except Exception, e:
                print e
            finally:
                self.f.close()

    def disconnect_client(self, List_box):
        '对应udp_server面板>侦听框架>客户端显示框架>断开按钮的函数，用于将某个客户端T掉'
        try:
            udp_client = List_box.get(List_box.curselection())
            yy = self.client_addr_list.index(udp_client)
            self.client_list[udp_client].close()
            List_box.delete(yy)
            self.client_conn_list.pop(yy)
            self.client_addr_list.pop(yy)
            self.client_list.pop(udp_client)
        except Exception, e:
            print e

    def clear_data_text(self, data_daxt, send_num_entry, receive_num_entry):
        '对应udp_server面板>统计框架>清空按钮的函数，用于清空接收和发送的数据，全部置为0'
        data_daxt.delete(0, data_daxt.size())
        self.send_num = 0
        send_num_entry.set(self.send_num)
        self.recv_num = 0
        receive_num_entry.set(self.recv_num)

    def send_data(self, send_entry_data, List_box, send_num_entry, data_text):
        '对应udp_server面板>发送数据框架>发送按钮的函数，用于向客户端发送带条数据'
        udp_client = List_box.get(List_box.curselection())
        print udp_client
        self.s.sendto(send_entry_data, udp_client)
        # 服务器发送给客户端的数据，同样显示在接收数据的框架里面
        data_text.insert(Tkinter.END, "%s [server>>%s] %d: %s\n" % (time.strftime("%H:%M:%S"), udp_client, len(send_entry_data),  send_entry_data))
        # 如果开启了日志功能，那么将发送给客户端的数据记录日志
        try:
            self.f.write("%s [server>>%s] %d: %s\n" % (time.strftime("%H:%M:%S"), udp_client, len(send_entry_data),  send_entry_data))
        except Exception, e:
            print e
        self.send_num += 1
        send_num_entry.set(self.send_num)

    def sent_data_timing_circulation_1(self, List_box, send_entry_data, send_interval, send_frame_button, send_num_entry, data_text, client_selected_1):
        'sent_data_timing_circulation_1，就是定时发送1函数拉起的线程对应的函数，用于循环形式发送数据'
        # 如果在这个线程里面不需要改变aa的值，那下面的global aa就不需要，同时aa不能在这里进行更改；
        # 在这里将aa置为全局变量，那么就可以在这里对aa进行赋值。
        global aa
        data_text.insert(Tkinter.END, "%s [server>>%s] %d: （定时发送1开始）%s\n" % (time.strftime("%H:%M:%S"), client_selected_1, len(send_entry_data),  send_entry_data))
        sleep_time = float(send_interval.get())/1000
        send_entry_data_all = ''
        wait_time = 0.0
        while aa:
            #下面的try，只要是用于当获取选中客户端失败、发送数据失败；可以将定时按钮重置；同时可以再次定时发送
            try:
                udp_client = List_box.get(List_box.curselection())
                while wait_time < 0.2 and len(send_entry_data_all) < 1400:
                    send_entry_data_all += send_entry_data
                    wait_time += sleep_time
                    self.send_num += 1
                    self.send_num_1 += 1
                    send_num_entry.set(self.send_num)
                    time.sleep(sleep_time)
                self.s.sendto(send_entry_data_all, udp_client)
                send_entry_data_all = ''
                wait_time = 0.0
            except Exception, e:
                data_text.insert(Tkinter.END, "%s [server>>%s] %d: （定时发送1结束, 发送次数%d）%s\n" % (time.strftime("%H:%M:%S"), client_selected_1, len(send_entry_data), self.send_num_1, send_entry_data))
                self.send_num_1 = 0
                aa = 0
                send_frame_button.set(u'定时发送')

    def send_data_timing_1(self, send_frame_button, send_entry_data, List_box, send_interval, send_num_entry, data_text):
        '对应udp_sever面板>发送数据大框架>发送数据小框架1>定时发送按钮的函数，用于向客户端定时发送数据'
        # 这个全局变量aa仅用于发送数据小框架1的定时发送，使用aa来对是否进行定时发送进行判断；aa作用于send_data_timing_1函数和
        # 由send_data_timing_1函数拉起的线程。
        # 点击“定时发送”>aa=1>拉起线程sent_data_timing_circulation_1>循环发送数据”
        # 点击“暂停”>因为这个时候“定时发送”按钮的值为“暂停”，也就是要暂停定时发送>aa=0>因为aa为全局变量，所以send_data_timing_circulation_1
        # 线程的aa同样也变成了0，while循环就用中断，定时发送就终止。
        global  aa, client_selected_1
        client_selected_1 = List_box.get(List_box.curselection())
        try:
            if send_frame_button.get() == u'定时发送' and List_box.get(List_box.curselection()):
                udp_client = List_box.get(List_box.curselection())
                aa = 1
                if send_interval.get().isdigit():
                    send_data_timing_thread = threading.Thread(target=self.sent_data_timing_circulation_1, args=(List_box, send_entry_data, send_interval,  send_frame_button, send_num_entry, data_text, client_selected_1))
                    send_data_timing_thread.start()
                    send_frame_button.set(u'暂停')
                else:
                    print u"请输入正整数"
            else:
                data_text.insert(Tkinter.END, "%s [server>>%s] %d: （定时发送1结束, 发送次数%d）%s\n" % (time.strftime("%H:%M:%S"), client_selected_1, len(send_entry_data), self.send_num_1, send_entry_data))
                self.send_num_1 = 0
                send_frame_button.set(u'定时发送')
                aa =0
        except Exception, e:
            send_frame_button.set(u'定时发送')
            print u"未选中客户端"

    def sent_data_timing_circulation_2(self, List_box, send_entry_data, send_interval, send_frame_button, send_num_entry, data_text, client_selected_2):
        'sent_data_timing_circulation_2，就是定时发送2函数拉起的线程对应的函数，用于循环形式发送数据'
        # 如果在这个线程里面不需要改变bb的值，那下面的global bb就不需要，同时bb不能在这里进行更改；
        # 在这里将bb置为全局变量，那么就可以在这里对bb进行赋值。
        global bb
        data_text.insert(Tkinter.END, "%s [server>>%s] %d: （定时发送2开始）%s\n" % (time.strftime("%H:%M:%S"), client_selected_2, len(send_entry_data),  send_entry_data))
        sleep_time = float(send_interval.get())/1000
        send_entry_data_all = ''
        wait_time = 0.0
        while bb:
            #下面的try，只要是用于当获取选中客户端失败、发送数据失败、插入数据到显示区域失败时；可以将定时按钮重置；同时可以再次定时发送
            try:
                udp_client = List_box.get(List_box.curselection())
                while wait_time < 0.2 and len(send_entry_data_all) < 1400:
                    send_entry_data_all += send_entry_data
                    wait_time += sleep_time
                    self.send_num += 1
                    self.send_num_2 += 1
                    send_num_entry.set(self.send_num)
                    time.sleep(sleep_time)
                self.s.sendto(send_entry_data_all, udp_client)
                send_entry_data_all = ''
                wait_time = 0.0
            except Exception, e:
                data_text.insert(Tkinter.END, "%s [server>>%s] %d: （定时发送2结束, 发送次数%d）%s\n" % (time.strftime("%H:%M:%S"), client_selected_2, len(send_entry_data), self.send_num_2, send_entry_data))
                self.send_num_2 = 0
                bb = 0
                send_frame_button.set(u'定时发送')

    def send_data_timing_2(self, send_frame_button, send_entry_data, List_box, send_interval, send_num_entry, data_text):
        '对应udp_sever面板>发送数据大框架>发送数据小框架1>定时发送按钮的函数，用于向客户端定时发送数据'
        # 这个全局变量bb仅用于发送数据小框架1的定时发送，使用aa来对是否进行定时发送进行判断；bb作用于send_data_timing_1函数和
        # 由send_data_timing_2函数拉起的线程。
        # 点击“定时发送”>bb=1>拉起线程sent_data_timing_circulation_2>循环发送数据”
        # 点击“暂停”>因为这个时候“定时发送”按钮的值为“暂停”，也就是要暂停定时发送>bb=0>因为bb为全局变量，所以send_data_timing_circulation_2
        # 线程的bb同样也变成了0，while循环就用中断，定时发送就终止。
        global  bb, client_selected_2
        client_selected_2 = List_box.get(List_box.curselection())
        try:
            if send_frame_button.get() == u'定时发送' and List_box.get(List_box.curselection()):
                udp_client = List_box.get(List_box.curselection())
                bb = 1
                if send_interval.get().isdigit():
                    send_data_timing_thread = threading.Thread(target=self.sent_data_timing_circulation_2, args=(List_box, send_entry_data, send_interval,  send_frame_button, send_num_entry, data_text, client_selected_2))
                    send_data_timing_thread.start()
                    send_frame_button.set(u'暂停')
                else:
                    print u"请输入正整数"
            else:
                data_text.insert(Tkinter.END, "%s [server>>%s] %d: （定时发送2结束, 发送次数%d）%s\n" % (time.strftime("%H:%M:%S"), client_selected_2, len(send_entry_data), self.send_num_2, send_entry_data))
                self.send_num_2 = 0
                send_frame_button.set(u'定时发送')
                bb =0
        except Exception, e:
            send_frame_button.set(u'定时发送')
            print u"未选中客户端"

    def sent_data_timing_circulation_3(self, List_box, send_entry_data, send_interval, send_frame_button, send_num_entry, data_text, client_selected_3):
        'sent_data_timing_circulation_3，就是定时发送2函数拉起的线程对应的函数，用于循环形式发送数据'
        # 如果在这个线程里面不需要改变cc的值，那下面的global cc就不需要，同时cc不能在这里进行更改；
        # 在这里将cc置为全局变量，那么就可以在这里对cc进行赋值。
        global cc
        data_text.insert(Tkinter.END, "%s [server>>%s] %d: （定时发送3开始）%s\n" % (time.strftime("%H:%M:%S"), client_selected_3, len(send_entry_data),  send_entry_data))
        sleep_time = float(send_interval.get())/1000
        send_entry_data_all = ''
        wait_time = 0.0
        while cc:
            #下面的try，只要是用于当获取选中客户端失败、发送数据失败时；可以将定时按钮重置；同时可以再次定时发送
            try:
                udp_client = List_box.get(List_box.curselection())
                while wait_time < 0.2 and len(send_entry_data_all) < 1400:
                    send_entry_data_all += send_entry_data
                    wait_time += sleep_time
                    self.send_num += 1
                    self.send_num_3 += 1
                    send_num_entry.set(self.send_num)
                    time.sleep(sleep_time)
                self.s.sendto(send_entry_data_all, udp_client)
                send_entry_data_all = ''
                wait_time = 0.0
            except Exception, e:
                data_text.insert(Tkinter.END, "%s [server>>%s] %d: （定时发送3结束, 发送次数%d）%s\n" % (time.strftime("%H:%M:%S"), client_selected_3, len(send_entry_data), self.send_num_3, send_entry_data))
                self.send_num_2 = 0
                cc = 0
                send_frame_button.set(u'定时发送')

    def send_data_timing_3(self, send_frame_button, send_entry_data, List_box, send_interval, send_num_entry, data_text):
        '对应udp_sever面板>发送数据大框架>发送数据小框架1>定时发送按钮的函数，用于向客户端定时发送数据'
        # 这个全局变量cc仅用于发送数据小框架1的定时发送，使用aa来对是否进行定时发送进行判断；cc作用于send_data_timing_3函数和
        # 由send_data_timing_3函数拉起的线程。
        # 点击“定时发送”>cc=1>拉起线程sent_data_timing_circulation_3>循环发送数据”
        # 点击“暂停”>因为这个时候“定时发送”按钮的值为“暂停”，也就是要暂停定时发送>cc=0>因为cc为全局变量，所以send_data_timing_circulation_3
        # 线程的cc同样也变成了0，while循环就用中断，定时发送就终止。
        global  cc, client_selected_3
        client_selected_3 = List_box.get(List_box.curselection())
        try:
            if send_frame_button.get() == u'定时发送' and List_box.get(List_box.curselection()):
                udp_client = List_box.get(List_box.curselection())
                cc = 1
                if send_interval.get().isdigit():
                    send_data_timing_thread = threading.Thread(target=self.sent_data_timing_circulation_3, args=(List_box, send_entry_data, send_interval,  send_frame_button, send_num_entry, data_text, client_selected_3))
                    send_data_timing_thread.start()
                    send_frame_button.set(u'暂停')
                else:
                    print u"请输入正整数"
            else:
                data_text.insert(Tkinter.END, "%s [server>>%s] %d: （定时发送2结束, 发送次数%d）%s\n" % (time.strftime("%H:%M:%S"), client_selected_3, len(send_entry_data), self.send_num_3, send_entry_data))
                self.send_num_3 = 0
                send_frame_button.set(u'定时发送')
                cc =0
        except Exception, e:
            send_frame_button.set(u'定时发送')
            print u"未选中客户端"


    def end_thread(self, list_box):
        # end_thread，该函数也非常有用；当侦听按钮从“停止”变“侦听”的时候，也就是服务器不再侦听时，由它来进行收尾工作
        self.signal = 0
        #下面的两句非常有用，当服务器开始侦听的时候，会拉起一个接收线程一直等待客户端连接过来；如果此时停止侦听，这个CONN, addr = s.accept()函数仍然在侦听，也就是说
        # 会占着ip+port不释放，也就是再进行下一轮的侦听；所以当停止侦听的时候，服务器电脑必须释放ip+port，否则无法侦听；
        # 因为在停止侦听的时候，仍然没有其他客户端连接过来；如果要将ip+port释放的话，就需要有客户端了解过来，让s.accept()跳出来；这里就是在本地，开启一个客户端，
        # 连接到服务器，让s.accept()跳出来，等它跳出来之后，s就可以正常close()了，端口也正常释放。
        c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        c.sendto('', (self.HOST, self.PORT))
        # 等待一段时间，让s有时间去释放端口
        time.sleep(0.02)
        c.close()
        #删除所有的客户端
        libt_box_len =  list_box.size()
        list_box.delete(0, libt_box_len)

    def Accept(self, data_text, receive_sum_entry, send_data, List_box):
        '由侦听函数拉起的线程对应的接收客户端连接的函数，用于接收客户端连接；当有客户端连接过来收，将ip+addr、socket等归类，便于后面的使用'
        # self.signal=1表明，是处于侦听状态；当self.signal=0时，就说明是停止侦听状态
        while self.signal:
            data, addr = self.s.recvfrom(1024)
            if addr not in self.client_addr_list:
                print 'zzzzzzzzzzzzzzzzzz'
                self.client_addr_list.append(addr)
                # 将客户端的ip+port插入到客户端列表框里面
                List_box.insert(Tkinter.END, addr)
            # 拉起线程，对应接收数据函数，用于实时接收数据
            if data != '':
                data_text.insert(Tkinter.END, "%s [%s>>server] %d: %s\n" % (time.strftime("%H:%M:%S"), addr, len(data),  data))
                try:
                    self.f.write("%s [%s>>server] %d: %s\n" % (time.strftime("%H:%M:%S"), addr, len(data),  data))
                except Exception, e:
                    print e
                #接收到一个数据，数据统计+1，并显示
                self.recv_num += 1
                receive_sum_entry.set(self.recv_num)
                #当接收到的数据超过了1024的时候，就将接收数据分区里面的第一行删除（也就是最早接收到的行）
                if self.recv_num > 1024:
                    data_text.delete(0)

    def Listen(self, param_list):
        '对应udp_server面板>侦听框架>侦听按钮的函数，用于udp_server的侦听；param_list就是从侦听按钮附带下来的参数的列表'
        # 这个s就是后面的socket，这里将其设置为全局变量，主要是用于出现异常时的处理
        global s
        if param_list[11].get() == u'侦听':
            try:
                # self.signal，对应侦听与否，当self.signal=0的时候，所有的连接等删除重置
                self.signal = 1
                self.HOST = param_list[9].get()
                self.PORT = int(param_list[10].get())
                #self.HOST = '192.168.150.1'
                #self.PORT = 20000
                self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                print 'open:',self.s._sock
                self.s.bind((self.HOST, self.PORT))
                # 如果这里直接使用s.accept()，那么s.accept()就会一直等待有客户端链接过来，如果没有，那么程序就会一直卡在这里，不会往下走；所以使用启用一个线程来实现
                # 服务器侦听动作
                # Accept函数，是整个udp_server里面的核心
                self.accept_thread = threading.Thread(target=self.Accept, args=(param_list[0], param_list[2], param_list[3].get(), param_list[12]))
                # thread.sedDaemon(True)，作用是将该thread设置父线程，当父线程被回收时，其下面的子线程都需要被回收。
                self.accept_thread.setDaemon(True)
                self.accept_thread.start()
                param_list[11].set(u'停止')
            except Exception, e:
                print e
        else:
            # 当点击“停止”按钮，所有的参数都重置
            param_list[11].set(u'侦听')
            self.end_thread(param_list[12])
            param_list[13].set(0)
            self.s.close()
            try:
                self.f.close()
            except:
                pass

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
9:self.ipaddr_entry
10:self.port_entry
11:self.listen_v
12:self.client_listbox
13:self.log_checkbutton_v
'''