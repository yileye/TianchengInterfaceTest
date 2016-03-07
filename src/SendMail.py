#coding=utf8
#######################################################
#filename: SendMail.py
#author: defias
#date: 2016-3
#function: send test report to email
#######################################################
from Global import *
import Config
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email.mime.application import MIMEApplication
from email import Utils, Encoders
import smtplib, socket

class SendMail(object):
    def __init__(self):
        send_emladdr = Config.ConfigIni.get_send_emladdr()
        PrintLog('debug','send_emladdr: %s', send_emladdr)
        self.to_addr = eval(send_emladdr)
        self.from_addr = 'yechaohui@tuandai.com'
        self.password = '****'
        self.smtp_server = 'smtp.exmail.qq.com'

    def getmsg(self, filename):
        '''
        构建邮件数据对象
        '''
        msg = MIMEMultipart('tiancheng testing report email')
        msg['From'] = self.from_addr
        msg['To'] = 'Recver <' + self.from_addr + '>'
        msg['Subject'] = u'来自天秤持续集成测试报告'
        msg['Date'] = Utils.formatdate(localtime = 1)
        msg['Message-ID'] = Utils.make_msgid()

        #邮件内容
        messagetext = u'''Dear All,
        Annex Libra continuous integration test report, please use the browser to open to view, thank you!
        '''
        parttext = MIMEText(messagetext)
        msg.attach(parttext)


        #文件附件
        filepart = MIMEApplication(open(filename,'rb').read())
        filepart.add_header('Content-Disposition', 'attachment', filename=filename.split("/")[-1])
        msg.attach(filepart)
        self.msg = msg
        return True

    def sendmail(self):
        try:
            if len(self.to_addr) == 0:
                return True
            server = smtplib.SMTP(self.smtp_server, 25)  #SMTP协议默认端口是25
            ehlocode = server.ehlo()[0]  #来自SMTP服务器数据形式的结果代码 正常:200~299
            if (200 <= ehlocode <= 299) and server.has_extn('starttls'):
                server.starttls()  #初始化加密信道

            PrintLog('info','login email: %s', self.from_addr)
            server.login(self.from_addr, self.password)
            server.sendmail(self.from_addr, self.to_addr, self.msg.as_string())  #可以一次发给多个人
            PrintLog('info','Email Message successfully sent')

        except (socket.gaierror, socket.error, socket.herror, smtplib.SMTPException), e:
            PrintLog('info','*** Your message may not hava been sent!')
            PrintLog('exception',e)
        return True
