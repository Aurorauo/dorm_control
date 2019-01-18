# -*- coding: utf-8 -*-
import bottle,requests
import time,serial
import threading,xlwt,xlrd
from xlutils.copy import copy
import pylab,numpy,os
from bottle import template,static_file

port='/dev/ttyUSB0'
ser=serial.Serial(port, 9600)

'''获取网页HTML文本'''
def get_text(url,sleep=0,timeout=5):
    try:
        time.sleep(float(sleep))
        header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
        'Content-Type': 'application/json',
        }
        r=requests.get(url,headers=header,timeout=float(timeout))
        r.encoding=r.apparent_encoding
        return r.text.replace('\n','').replace('\t','').replace('\r','').replace(' ','')
    except:
        return ''
'''获取网页二进制结果'''
def get_content(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
        'Content-Type': 'application/json',
        }
    r=requests.get(url,headers=header)
    r.encoding=r.apparent_encoding
    return r.content
def plot(num,xdata,ydata,title,xlabel,ylabel,grid=True):
    pylab.figure(num)
    pylab.title(title,fontsize=20)  #图表的名称
    pylab.xlabel(xlabel,fontsize=10) #图表X坐标轴名称
    pylab.ylabel(ylabel,fontsize=10)  #图表Y坐标轴名称
    pylab.plot(xdata,ydata,'b-')#画线
    pylab.plot(xdata,ydata,'r.')#标出相关的点
    pylab.grid(grid)#网格生效
    pylab.savefig('images/temp.png')  #图片保存位置
    
@bottle.route('/dorm', method='GET')
def data():
    ser.write('t')
    temp=ser.readline()
    page='''<!doctype html>
    <html>
    <head>
    <meta charset="utf8">
    <title>智慧宿舍</title>
    </head>
    <body>'''
    return page+'''<center><h1><font size="12" color="red">寝室实时温度为>>'''+str(temp)+'''摄氏度</font></h1></center></body></html>'''

@bottle.route('/temp', method='GET')
def plot_data():
    data=xlrd.open_workbook('data.xls')
    table=data.sheets()[0]
    TT=table.col_values(1)[1:]
    tt=table.col_values(0)[1:]
    date=table.col_values(2)[1:]
    T=[]
    t=[]
    d=[]
    n=0
    for i in date:
        if str(i)[:10]==str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))[:10]:
            T.append(TT[n])
            t.append(tt[n])
            d.append(i[11:-3])
        n=n+1
    xlabel='time  [interval > 2 min   start time > '+str(d[0])+']'
    plot(1,t,T,"temperature trend figure",xlabel,'temperature [ degree Celsius ]')
    text='''<html>
    <head>
        <title></title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <style type="text/css">
            h2
            {
                margin-top:4%;
                margin-bottom:40px;
            }
        </style>
    </head>
    <body>
        <center>
        <h2><a href="/login"><center>欢迎登录寝室网络管理平台</center></a></h2><br/><br/><p><font size="4"> <center>寝室内温度变化趋势图</center></font>'''
    text=text+'''<center><img src="/images/temp.png" width="100%" /></center></center>'''
    text=text+'''
    </body>
</html>'''
    return text
    
@bottle.route('/images/<filename:re:.*\.css|.*\.js|.*\.png|.*\.jpg|.*\.gif>', method='GET')
def server_static(filename):
    """定义/assets/下的静态(css,js,图片)资源路径"""
    return static_file(filename, root='./images')

@bottle.route('/login', method='GET')
def plot_data():
    page='''<html>
    <head>
        <title></title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <style type="text/css">
            h2
            {
                margin-top:4%;
                margin-bottom:40px;
            }
        </style>
    </head>
    <body>
        <center>
        <h2>欢迎登录寝室网络管理平台</h2>
            <form action="/login" method="post" accept-charset="utf-8">
                <p>用户名: <input type="text" name="name"  /></p> 
                <p>密 码:  <input type="password" name="pwd"  /></p>
                <input type="submit" value="登录"  />        
                 
            </form>
        </center>
    </body>
</html>
'''
    return page
@bottle.route('/login', method='POST')
def plot_data():
    name=bottle.request.forms.get('name')
    psd=bottle.request.forms.get('pwd')
    t=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    try:
        led=bottle.request.forms.get('led')
        if str(led)=='ON':
            ser.write(bytes('b',encoding='utf8'))
        elif str(led)=='OFF':
            ser.write(bytes('a',encoding='utf8'))
    except:
        pass
    try:
        if (name==u'zf' and psd==u'hfutzf') or led:
            page='''<html>
    <head>
        <title>寝室网络管理平台</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <style type="text/css">
            h2
            {
                margin-top:4%;
                margin-bottom:40px;
            }
        </style>
    </head>
    <body>
        <center>
        <h2>欢迎使用智能寝室网络-控制平台</h2>
        <center><p><font size="4" color="blue">当前实时时间&nbsp;&nbsp;'''
            page=page+str(t)+'''</font></p></center>'''
            ser.write(bytes('m',encoding='utf8'))
            state=str(ser.readline(),encoding='utf8').replace('\r','').replace('\t','').replace('\n','')
            if int(state)==0:
                sta='关闭'
            elif int(state)==1:
                sta='开启'
            ser.write(bytes('t',encoding='utf8'))
            temp=str(ser.readline(),encoding='utf8').replace('\r','').replace('\t','').replace('\n','')
            page=page+'''<center><p><font size="4" color="green"><a href="/temp">寝室实时温度为>&nbsp;&nbsp;'''+str(temp)+'''&nbsp;&nbsp;摄氏度</a></font></p></center>'''
            page=page+'''<center><p><font size="4" color="green">Led状态为>&nbsp;&nbsp;'''+str(sta)+'''<br/><br/><br/><br/><br/><br/></font></p></center>'''
            page=page+'''
               <center>
        
            <form  method="post" accept-charset="utf-8">
                <p>LED开关按钮:&nbsp;&nbsp;<input type="Submit" value="ON" name="led" style='background-color:green'/> &nbsp;&nbsp;&nbsp;<input type="Submit" value="OFF" name="led" style='background-color:red'/></p> 
               <br/><br/><br/><center><p><font size="4"> 寝室内温度变化趋势图</font><br/>  <img src="/images/temp.png" width="100%"/></p></center>
            </form>
        </center>
        </center>
    </body>
</html>
'''
            return page
        else:
            return '''<h1>您没有权限访问</h1>'''
    except:
        return '''<h1>some error occurs</h1>'''

def monitor():
    while 1:
        t=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        date=time.localtime()
        if 1:
            if float(date.tm_min)//2==float(date.tm_min)/2 and str(date.tm_sec)=='10':
                if not(os.path.exists('data.xls')):
                    w=xlwt.Workbook()
                    h=30
                    sheet =w.add_sheet("command_data")
                    style = xlwt.easyxf('font: bold 1, color red;')
                    sheet.write(0,0,u"记录序号",style)
                    sheet.write(0,1,u"温度值（单位：摄氏度）",style)
                    sheet.write(0,2,u"温度值写入时间",style)
                    sheet.col(0).width = 256 *10
                    sheet.col(1).width = 256 *h
                    sheet.col(2).width = 256 *h
                    w.save('data.xls')
                old = xlrd.open_workbook('data.xls',formatting_info=True)
                new = copy(old)
                news = new.get_sheet(0)
                sheet_data=old.sheet_by_index(0)
                n=sheet_data.nrows
                news.write(n,0,float(n))
                ser.write(bytes('t',encoding='utf8'))
                temp=str(ser.readline(),encoding='utf8').replace('\r','').replace('\t','').replace('\n','')
                news.write(n,1,float(temp))
                news.write(n,2,t)
                new.save('data.xls')
                time.sleep(1)
        else:
            pass
            
threads = []
gg = threading.Thread(target=monitor)                      
threads.append(gg)
                    
if __name__ == '__main__':
    for i in threads:
        i.start()
    bottle.run(host='0.0.0.0', port=10834)
