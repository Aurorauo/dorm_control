# -*- coding: utf-8 -*-
import bottle,requests
import time,serial

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
            ser.write('b')
        elif str(led)=='OFF':
            ser.write('a')
    except:
        pass
    try:
        if (name==u'**' and psd==u'****') or led:
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
            ser.write('m')
            state=ser.readline()
            if int(state)==0:
                sta='关闭'
            elif int(state)==1:
                sta='开启'
            ser.write('t')
            temp=ser.readline()
            page=page+'''<center><p><font size="4" color="green">寝室实时温度为>&nbsp;&nbsp;'''+str(temp)+'''&nbsp;&nbsp;摄氏度\n</font></p></center>'''
            page=page+'''<center><p><font size="4" color="green">Led状态为>&nbsp;&nbsp;'''+str(sta)+'''<br/><br/><br/><br/><br/><br/></font></p></center>'''
            page=page+'''
                <center>
        
            <form  method="post" accept-charset="utf-8">
                <p>LED开关按钮:&nbsp;&nbsp;<input type="Submit" value="ON" name="led" style='background-color:green'/> &nbsp;&nbsp;&nbsp;<input type="Submit" value="OFF" name="led" style='background-color:red'/></p> 
                
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
        return '''<h1>您没有权限访问</h1>'''

if __name__=="__main__":
    bottle.run(host='0.0.0.0', port=10834)
