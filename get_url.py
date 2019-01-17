# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 21:29:44 2019

@author: Administrator
"""
from selenium import webdriver
import re,time

from email.mime.multipart import MIMEMultipart  
from email.mime.application import MIMEApplication  
from email.mime.text import MIMEText  
import smtplib

class send():
    def __init__(self,fro,psd,to,serve,subject,content):
       self.msg_from=fro                                #发送方邮箱
       self.passwd=psd                                   #填入发送方邮箱的授权码
       self.msg_to=to                                #收件人邮箱
                                
       self.subject=subject                                     #主
       
      
       self.content=content
       self.msg = MIMEText(self.content)
       self.msg['Subject'] = self.subject
       self.msg['From'] = self.msg_from
       self.msg['To'] = self.msg_to
       self.s=smtplib.SMTP_SSL(serve,465)
       self.s.login(self.msg_from, self.passwd)
       self.s.sendmail(self.msg_from, self.msg_to, self.msg.as_string())
       self.s.quit()
       
def cploar():
    browser = webdriver.Chrome(executable_path=r'C:\chromedriver\chromedriver.exe')
    browser.get('https://dashboard.cpolar.com/login')
    browser.find_element_by_xpath('//*[@id="captcha-form"]/fieldset/div[1]/div/div/input').send_keys('1379875051@qq.com')
    browser.find_element_by_xpath('//*[@id="password"]').send_keys('bh123456')
    browser.find_element_by_xpath('//*[@id="loginBtn"]').click()
    time.sleep(1)
    browser.get('https://dashboard.cpolar.com/status')
    text=browser.page_source.replace(' ','').replace('\n','').replace('\r','').replace('\t','')
    print(text)
    urls=re.compile('<thscope="row"><ahref=".*?"target="_blank">(.*?)</a></th><td>.*?</td><td>(.*?)</td><td>(.*?)</td>').findall(text)
    browser.quit()
    return urls
while 1:
    t=time.localtime()
    if float(t.tm_min)//5==float(t.tm_min)/5 and str(t.tm_sec)=='10':
        print(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))+'  >程序正在运行')
        time.sleep(1)
    try:
        if str(t.tm_hour)=='0' and str(t.tm_min)=='10':
            urls=cploar()
            if len(urls)!=0:
                text='您好：\n\n   最新的更新链接如下所示,更新时间：'+str(urls[0][2])+'\n\n   '
                for i in urls:
                    text=text+i[0]+'\n\n   '
                text=text+'\n\n\n  【备注：由程序自动编写和发送，勿回复！！！】'
            else:
                text='您好：\n\n   您并未开启任何隧道服务，请开通一个至少隧道！！\n\n\n  【备注：由程序自动编写和发送，勿回复！！！】'
            send('codetest@126.com','hfutzf083415','1379875051@qq.com',"smtp.126.com",'cploar更换网址快讯',text)  
            time.sleep(60)
    except:
        pass
            
