# -*- coding:utf-8 -*-
__author__ = 'Administrator'

'''
这个模块的功能是对一整块frame进行划分，划分成“侦听部分”、“数据发送部分”、“数据统计部分”、“数据接收部分”
所以，这个模块的所有函数，都需要“整块frame”这个参数；都是在“整块frame”的基础上再次进行细分。
'''
import Tkinter
from tcp_server_function import Tcp_Server_Function

class Tcp_Server_Frame_Divide():
    def __init__(self):
        '''
        1.main脚本调用Tcp_Server_Frame_Divide类的第一个步骤，就是实例话tcp_server_function类；
        2.即使tcp_server_function类是空的，也不影响tcp_Server面板的形成，结果就是只有面板，没有相应的功能。
        '''
        self.TSF = Tcp_Server_Function()

    def receive_partion(self, Frame):
        '''
        1.receive_partion是tcp_server面板里面显示接收到的数据的组件；
        2.注意到这里的Frame，指的是整个tcp_server框架，其他所有的子框架都是基于此。
        '''
        receive_frame = Tkinter.Frame(Frame)
        # 1.下面的语句，height=600，可能已经大于了整个工具设定的高度；但没有关系，它可以随着整个工具的高度来自动变化；
        # 2.exportselection=Tkinter.FALSE,整个参数尤其重要，如果listbox里面有参数被选定，那么bg就是置为蓝色；如果整个时候用鼠标
        # 取选中其他组件里面的参数，那么listbox里面被选中的参数就会变为未被选中；加上exportselection=Tkinter.FALSE,listbox里面
        # 被选中的参数就不会“去选中”，保持选中状态。
        # 3.整个listbox组件是建立在receive_frame里面的

        # 下面的几行，就是将X和Y方形的滚动条绑定在listbox上面
        self.sl_vertical = Tkinter.Scrollbar(receive_frame, orient=Tkinter.VERTICAL)  #文本框-竖向滚动条
        self.sl_horizontal = Tkinter.Scrollbar(receive_frame, orient=Tkinter.HORIZONTAL)
        self.data_text = Tkinter.Listbox(receive_frame, height=600, exportselection=Tkinter.FALSE,
                                         yscrollcommand=self.sl_vertical.set, xscrollcommand=self.sl_horizontal.set)
        self.sl_vertical.config(command=self.data_text.yview)
        self.sl_horizontal.config(command=self.data_text.xview)
        self.sl_vertical.pack(fill=Tkinter.Y, expand=0, side=Tkinter.RIGHT, anchor=Tkinter.N)
        self.sl_horizontal.pack(fill=Tkinter.X, expand=0, side=Tkinter.BOTTOM, anchor=Tkinter.N)

        # 创建一个菜单>菜单添加“copy”按钮>data_text区域绑定右键行为
        self.menubar = Tkinter.Menu(self.data_text)
        self.menubar.add_command(label='copy', command=self.copy_data)
        self.data_text.bind('<Button-3>', self.popup)
        self.data_text.pack(fill=Tkinter.BOTH, expand=1, side=Tkinter.LEFT)

        #self.data_text.pack(fill=Tkinter.BOTH, expand=1,padx=5)
        receive_frame.pack(fill=Tkinter.BOTH, expand=1)

    def popup(self, event):
        '数据区的鼠标行为，这是listbox绑定的是右键<Button-3>'
        self.menubar.post(event.x_root, event.y_root)

    def copy_data(self):
        'copy_data函数，用于数据区鼠标右键里面的元素的行为'
        # clipboad在每个组件里面都有，表示的是剪切板内容，是复制内容暂时存放的地方；
        # clear动作是清空剪切板，append动作是追加到剪切板
        self.data_text.clipboard_clear()
        # self.data_text.curselection()返回的序号，get(index)返回的是选中的内容
        self.data_text.clipboard_append(self.data_text.get(self.data_text.curselection()))

    def statistical_partion(self, Frame):
        'statistical_partion：从整块frame当中挖出一块用于实现统计数据的发送和结束条数总和的框架'
        statistical_frame = Tkinter.Frame(Frame)
        self.send_num_label = Tkinter.Label(statistical_frame, text=u'发送:')
        self.send_num_label.pack(side=Tkinter.LEFT,padx=5)
        # 整个self.send_num是会变的，所以要用Tkinter.STringVar()来指定它的属性
        self.send_num = Tkinter.StringVar()
        # 注意变量的用法，textvariable=self.send_num
        self.send_num_entry = Tkinter.Entry(statistical_frame, textvariable=self.send_num, width=10)
        # 下面语句的作用是设置send_num_entry为只读模式，不可手动更改
        self.send_num_entry['state'] = 'readonly'
        self.send_num_entry.pack(side=Tkinter.LEFT,padx=5)
        self.receive_num_label = Tkinter.Label(statistical_frame, text=u'接收:')
        self.receive_num_label.pack(side=Tkinter.LEFT,padx=5)
        self.receive_num = Tkinter.StringVar()
        self.receive_num_entry = Tkinter.Entry(statistical_frame, textvariable=self.receive_num, width=10)
        self.receive_num_entry['state'] = 'readonly'
        self.receive_num_entry.pack(side=Tkinter.LEFT,padx=5)
        self.clear_button = Tkinter.Button(statistical_frame, text=u'清空', command=lambda : self.TSF.clear_data_text(self.data_text, self.send_num, self.receive_num), width=10)
        self.clear_button.pack(side=Tkinter.RIGHT,padx=5)
        self.log_checkbutton_v = Tkinter.StringVar()
        self.log_checkbutton_v.set(0)
        self.log_checkbutton = Tkinter.Checkbutton(statistical_frame, text=u'日志', variable=self.log_checkbutton_v, command=lambda : self.TSF.log_recode(self.log_checkbutton_v, ), width=10)
        self.log_checkbutton.pack(side=Tkinter.RIGHT,padx=5)
        statistical_frame.pack(pady=5, fill=Tkinter.X)

    def send_partion_1(self, send_frame):
        'send_partion_signal：用于在“整个数据发送frame”中实现一块小的数据发送区域'
        send_frame_1 = Tkinter.Frame(send_frame)
        self.send_frame_label_1 = Tkinter.Label(send_frame_1, text=u'数据1:')
        self.send_frame_label_1.pack(side=Tkinter.LEFT,padx=5)
        self.send_frame_entry_1 = Tkinter.Entry(send_frame_1)
        self.send_frame_entry_1.pack(side=Tkinter.LEFT,padx=5, expand=1, fill=Tkinter.X)
        # 1.发送按钮，对应将数据发送出去；就需要有相应的函数支撑，格式是command=函数名；
        # 2.如果格式是command=函数名()，那么在面板形成的时候，这个函数就会执行一次；同时以后再点击这个按钮，没有任何效果；
        # 3.如果函数需要带参数，那么要使用这样的格式command=lambda : 函数名(参数)
        self.send_frame_button_1 = Tkinter.Button(send_frame_1, text=u'发送', command=lambda : self.TSF.send_data(self.send_frame_entry_1.get(), self.client_listbox, self.send_num, self.data_text), width=10)
        self.send_frame_button_1.pack(side=Tkinter.LEFT, padx=5)
        self.listen_v_send_timing_1 = Tkinter.StringVar()
        self.listen_v_send_timing_1.set(u'定时发送')
        self.send_timing_frame_button_1 = Tkinter.Button\
            (send_frame_1, textvariable=self.listen_v_send_timing_1, command=lambda : self.TSF.send_data_timing_1(self.listen_v_send_timing_1, self.send_frame_entry_1.get(), self.client_listbox, self.send_timing_frame_entry_1, self.send_num, self.data_text), width=10)
        self.send_timing_frame_button_1.pack(side=Tkinter.LEFT, padx=5)
        self.send_timing_frame_entry_1 = Tkinter.Entry(send_frame_1, width=10)
        self.send_timing_frame_entry_1.pack(side=Tkinter.LEFT,padx=5)
        self.send_timing_frame_label_1 = Tkinter.Label(send_frame_1, text='ms')
        self.send_timing_frame_label_1.pack()
        send_frame_1.pack(pady=3, expand=1, fill=Tkinter.X)

    def send_partion_2(self, send_frame):
        'send_partion_signal：用于在“整个数据发送frame”中实现一块小的数据发送区域'
        send_frame_2 = Tkinter.Frame(send_frame)
        self.send_frame_label_2 = Tkinter.Label(send_frame_2, text=u'数据2:')
        self.send_frame_label_2.pack(side=Tkinter.LEFT,padx=5)
        self.send_frame_entry_2 = Tkinter.Entry(send_frame_2)
        self.send_frame_entry_2.pack(side=Tkinter.LEFT,padx=5, expand=1, fill=Tkinter.X)
        self.send_frame_button_2 = Tkinter.Button(send_frame_2, text=u'发送', command=lambda : self.TSF.send_data(self.send_frame_entry_2.get(), self.client_listbox, self.send_num, self.data_text), width=10)
        self.send_frame_button_2.pack(side=Tkinter.LEFT, padx=5)
        self.listen_v_send_timing_2 = Tkinter.StringVar()
        self.listen_v_send_timing_2.set(u'定时发送')
        self.send_timing_frame_button_2 = Tkinter.Button\
            (send_frame_2, textvariable=self.listen_v_send_timing_2, command=lambda : self.TSF.send_data_timing_2(self.listen_v_send_timing_2, self.send_frame_entry_2.get(), self.client_listbox, self.send_timing_frame_entry_2, self.send_num, self.data_text), width=10)
        self.send_timing_frame_button_2.pack(side=Tkinter.LEFT, padx=5)
        self.send_timing_frame_entry_2 = Tkinter.Entry(send_frame_2, width=10)
        self.send_timing_frame_entry_2.pack(side=Tkinter.LEFT,padx=5)
        self.send_timing_frame_label_2 = Tkinter.Label(send_frame_2, text='ms')
        self.send_timing_frame_label_2.pack()
        send_frame_2.pack(pady=3, expand=1, fill=Tkinter.X)

    def send_partion_3(self, send_frame):
        'send_partion_signal：用于在“整个数据发送frame”中实现一块小的数据发送区域'
        send_frame_3 = Tkinter.Frame(send_frame)
        self.send_frame_label_3 = Tkinter.Label(send_frame_3, text=u'数据3:')
        self.send_frame_label_3.pack(side=Tkinter.LEFT,padx=5)
        self.send_frame_entry_3 = Tkinter.Entry(send_frame_3)
        self.send_frame_entry_3.pack(side=Tkinter.LEFT,padx=5, expand=1, fill=Tkinter.X)
        self.send_frame_button_3 = Tkinter.Button(send_frame_3, text=u'发送', command=lambda : self.TSF.send_data(self.send_frame_entry_3.get(), self.client_listbox, self.send_num, self.data_text), width=10)
        self.send_frame_button_3.pack(side=Tkinter.LEFT, padx=5)
        self.listen_v_send_timing_3 = Tkinter.StringVar()
        self.listen_v_send_timing_3.set(u'定时发送')
        self.send_timing_frame_button_3 = Tkinter.Button\
            (send_frame_3, textvariable=self.listen_v_send_timing_3, command=lambda : self.TSF.send_data_timing_3(self.listen_v_send_timing_3, self.send_frame_entry_3.get(), self.client_listbox, self.send_timing_frame_entry_3, self.send_num, self.data_text), width=10)
        self.send_timing_frame_button_3.pack(side=Tkinter.LEFT, padx=5)
        self.send_timing_frame_entry_3 = Tkinter.Entry(send_frame_3, width=10)
        self.send_timing_frame_entry_3.pack(side=Tkinter.LEFT,padx=5)
        self.send_timing_frame_label_3 = Tkinter.Label(send_frame_3, text='ms')
        self.send_timing_frame_label_3.pack()
        send_frame_3.pack(pady=3, expand=1, fill=Tkinter.X)

    def send_partion(self, Frame):
        'send_partion：从整块frame当中挖出一块用于实现数据发送部分的框架'
        # 需要将上面三个发送小区域应用起来
        send_frame = Tkinter.Frame(Frame)
        self.send_partion_1(send_frame)
        self.send_partion_2(send_frame)
        self.send_partion_3(send_frame)
        #fill=Tkinter.X，允许send_frame向X方向填充
        send_frame.pack(pady=5, fill=Tkinter.X)

    def listen_partion(self, Frame):
        'listen_partion：从整块frame当中挖出一块用于实现服务器侦听部分的框架'
        listen_frame = Tkinter.Frame(Frame)
        #整个侦听区域分成两块：服务器设置区域和客户端显示区域
        server_frame = Tkinter.Frame(listen_frame)
        client_frame = Tkinter.Frame(listen_frame)

        self.ipaddr_label = Tkinter.Label(server_frame, text=u'服务器IP:')
        self.ipaddr_label.pack(side=Tkinter.LEFT, padx=5)
        self.ipaddr_entry = Tkinter.Entry(server_frame)
        self.ipaddr_entry.pack(side=Tkinter.LEFT, padx=10)
        self.port_label = Tkinter.Label(server_frame, text=u'服务器port:')
        self.port_label.pack(side=Tkinter.LEFT, padx=5)
        self.port_entry = Tkinter.Entry(server_frame)
        self.port_entry.pack(side=Tkinter.LEFT, padx=5)
        self.listen_v = Tkinter.StringVar()
        self.listen_v.set(u'侦听')
        self.listen_button = Tkinter.Button(server_frame, textvariable=self.listen_v, command=lambda : self.TSF.Listen(self.paramater_list()), width=10)
        self.listen_button.pack(side=Tkinter.LEFT, padx=5)

        self.client_listbox = Tkinter.Listbox(client_frame, height=5, width=30, exportselection=Tkinter.FALSE)
        self.client_listbox.pack(side=Tkinter.LEFT, fill=Tkinter.X, expand=1)
        self.disconnect_button = Tkinter.Button(client_frame, text=u'断开', command=lambda : self.TSF.disconnect_client(self.client_listbox, ), width=10)
        self.disconnect_button.pack(side=Tkinter.RIGHT, padx=5)

        server_frame.pack(fill=Tkinter.BOTH, expand=1, side=Tkinter.LEFT)
        client_frame.pack(side=Tkinter.RIGHT, fill=Tkinter.X, expand=1)
        listen_frame.pack(fill=Tkinter.X)

    def connect_partion(self, Frame):
        'connect_partion：从整块frame当中挖出一块用于实现客户端连接部分的框架'
        connect_frame = Tkinter.Frame(Frame)
        server_frame = Tkinter.Frame(connect_frame)

        self.ipaddr_server_label = Tkinter.Label(server_frame, text=u'服务器IP:')
        self.ipaddr_server_label.pack(side=Tkinter.LEFT, padx=5)
        self.ipaddr_server_entry = Tkinter.Entry(server_frame)
        self.ipaddr_server_entry.pack(side=Tkinter.LEFT, padx=10)
        self.port_server_label = Tkinter.Label(server_frame, text=u'服务器port:')
        self.port_server_label.pack(side=Tkinter.LEFT, padx=5)
        self.port_server_entry = Tkinter.Entry(server_frame)
        self.port_server_entry.pack(side=Tkinter.LEFT, padx=5)
        self.connect_button = Tkinter.Button(server_frame, text=u'连接', width=10)
        self.connect_button.pack(side=Tkinter.LEFT, padx=5)
        server_frame.pack(fill=Tkinter.BOTH, expand=1, side=Tkinter.LEFT)
        connect_frame.pack(fill=Tkinter.X)

    def paramater_list(self):
        'paramater_list：以列表的形式，将面板中的各类entry、listbox、StringVar（各种变量）传入函数里面，以便于在函数里面对面板的各个组件进行赋值等'
        return [self.data_text, self.send_num, self.receive_num, self.send_frame_entry_1, self.send_timing_frame_entry_1, self.send_frame_label_2,
                self.send_timing_frame_entry_2, self.send_frame_entry_3, self.send_timing_frame_entry_3, self.ipaddr_entry, self.port_entry, self.listen_v,
                self.client_listbox, self.log_checkbutton_v]



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