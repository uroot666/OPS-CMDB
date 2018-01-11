#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 实现邮件发送功能

import sys
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
 
my_sender = '*******'    # 发件人邮箱账号
my_pass = '*******'      # 发件人邮箱密码

def mail(my_user, content_subject, content):
    ret=True
    try:
        msg=MIMEText(content,'html','utf-8')
        msg['From']=formataddr(["监控服务器",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To']=formataddr(["报警接收人",my_user])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = content_subject                # 邮件的主题，也可以说是标题
 
        server=smtplib.SMTP("smtp.163.com", 25)  # 发件人邮箱中的SMTP服务器，端口是25
        # server=smtplib.SMTP_SSL("smtp.163.com", 465) # 发件人邮箱中的SMTP服务器，SSL 端口为465
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender,my_user,msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret=False
    return ret

if __name__ == '__main__':
    # if len(sys.argv) < 3:
    #     raise '参数应该为：主题 内容'
    RET = mail('liangbiao666@gmail.com', '资源告警', 'a<br/>b')
    # ret=mail(sys.argv[1], sys.argv[2])
    if RET:
        print("邮件发送成功")
    else:
        print("邮件发送失败")