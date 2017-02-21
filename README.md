# TCP-UDP-socket
使用python编写tcp-udp工具，可及时修改代码，以便过滤需要的数据

第一步：通过Tkinter分别实现TCP-server、UDP-server、TCP-client、UDP-client的框架；

第二步：将四个框架组合在一起，形成工具模式的图形化界面（这里特别要注意的是，当显示一个框架时，其他三个框架要forget；否则图形工具会显示最后一个框架）；

第三步：根据import socket的原理来实现各类服务（这一步，有几个关键点需要注意：server停止侦听时，端口的回收；多线程双向通信）
