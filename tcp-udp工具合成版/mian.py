# -*- coding:utf-8 -*-
__author__ = 'Administrator'

import Tkinter
from tcp_server_frame_divide import Tcp_Server_Frame_Divide
from udp_server_frame_divide import Ucp_Server_Frame_Divide
from tcp_client_frame_divide import Tcp_Client_Frame_Divide
from udp_client_frame_divide import Udp_Client_Frame_Divide

root = Tkinter.Tk()
root.title(u"TCP-UDP工具")
root.geometry('1000x600')

Frame_module = Tkinter.Frame(root)
Frame_content = Tkinter.Frame(root)

def tcp_server_butuon():
    udp_server_frame.forget()
    tcp_client_frame.forget()
    udp_client_frame.forget()
    tcp_server_frame.pack(fill=Tkinter.BOTH, expand=1)
    tcp_client_frame.pack_forget()
def udp_server_butuon():
    tcp_server_frame.forget()
    tcp_client_frame.forget()
    udp_client_frame.forget()
    udp_server_frame.pack(fill=Tkinter.BOTH, expand=1)
def tcp_client_butuon():
    tcp_server_frame.forget()
    udp_server_frame.forget()
    udp_client_frame.forget()
    tcp_client_frame.pack(fill=Tkinter.BOTH, expand=1)
def udp_client_butuon():
    tcp_server_frame.forget()
    udp_server_frame.forget()
    tcp_client_frame.forget()
    udp_client_frame.pack(fill=Tkinter.BOTH, expand=1)

v = Tkinter.IntVar()
v.set(1)
Tkinter.Radiobutton(Frame_module, variable=v, value=1, text='TCP服务器', indicatoron=0, relief='ridge', command=tcp_server_butuon, width=25).pack(side=Tkinter.LEFT)
Tkinter.Radiobutton(Frame_module, variable=v, value=2, text='UDP服务器', indicatoron=0, relief='ridge', command=udp_server_butuon, width=25).pack(side=Tkinter.LEFT)
Tkinter.Radiobutton(Frame_module, variable=v, value=3, text='TCP客户端', indicatoron=0, relief='ridge', command=tcp_client_butuon, width=25).pack(side=Tkinter.LEFT)
Tkinter.Radiobutton(Frame_module, variable=v, value=4, text='UDP客户端', indicatoron=0, relief='ridge', command=udp_client_butuon, width=25).pack(side=Tkinter.LEFT)

#先建四个框架，分别对应tcp server、udp server、tcp client、udp-client
tcp_server_frame = Tkinter.Frame(Frame_content)
udp_server_frame = Tkinter.Frame(Frame_content)
tcp_client_frame = Tkinter.Frame(Frame_content)
udp_client_frame = Tkinter.Frame(Frame_content)

#下面四句实现tcp_server的面板
FD_tcp_server = Tcp_Server_Frame_Divide()
FD_tcp_server.listen_partion(tcp_server_frame)
FD_tcp_server.send_partion(tcp_server_frame)
FD_tcp_server.statistical_partion(tcp_server_frame)
FD_tcp_server.receive_partion(tcp_server_frame)
# #下面四句实现udp_server的面板
FD_udp_server = Ucp_Server_Frame_Divide()
FD_udp_server.listen_partion(udp_server_frame)
FD_udp_server.send_partion(udp_server_frame)
FD_udp_server.statistical_partion(udp_server_frame)
FD_udp_server.receive_partion(udp_server_frame)
# #下面四句实现tcp_client的面板
FD_tcp_client = Tcp_Client_Frame_Divide()
FD_tcp_client.connect_partion(tcp_client_frame)
FD_tcp_client.send_partion(tcp_client_frame)
FD_tcp_client.statistical_partion(tcp_client_frame)
FD_tcp_client.receive_partion(tcp_client_frame)
# #下面四句实现udp_client的面板
FD_udp_client = Udp_Client_Frame_Divide()
FD_udp_client.connect_partion(udp_client_frame)
FD_udp_client.send_partion(udp_client_frame)
FD_udp_client.statistical_partion(udp_client_frame)
FD_udp_client.receive_partion(udp_client_frame)

Frame_module.pack(pady=5, fill=Tkinter.X, padx=5)
tcp_server_frame.pack(fill=Tkinter.BOTH, expand=1)
udp_server_frame.pack(fill=Tkinter.BOTH, expand=1)
tcp_client_frame.pack(fill=Tkinter.BOTH, expand=1)
udp_client_frame.pack(fill=Tkinter.BOTH, expand=1)
Frame_content.pack(pady=5, fill=Tkinter.BOTH, expand=1)

root.mainloop()