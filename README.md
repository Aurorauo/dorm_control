### dorm_control
通过网页对寝室电器设备进行控制

1、用到的硬件有：树莓派3B+、arduino uno、TTL转串口、温度传感器、其他辅助件（面包板、排线等）

2、cploar.txt中命令用于配置http监听端口

3、sessor.ino为arduino中所烧程序的源代码，用于读取温度传感器所测的值、串口通讯和控制LED的亮和灭

4、web_page.py是控制平台网页前台和后台的源代码

5、get_url.py用来爬取cploar所分配的免费二级域名，并所爬到数据发送到邮箱【每晚十二点多左右自动更换域名】
