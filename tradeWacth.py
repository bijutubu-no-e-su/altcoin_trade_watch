# -*- coding: utf-8 -*-
import os, json
import python_bitbankcc
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from time import sleep
import requests

class orders:
    pair=""     #通貨ペア
    p=""        #apiオブジェクト
    dict1 = {}  #取引idsリスト
    def __init__(self,x,y):
        self.p = x
        self.pair=y
        self.getNewList()
    def getNewList(self):
        v=self.p.get_active_orders(self.pair)
        for f in v['orders']:
            a=f['order_id']
            if not a in self.dict1.keys():
                self.dict1[a] = a
                print('追加： side:%s price:%s amount:%s' % (f['side'],f['price'],f['start_amount']))
    def CheckList(self):
        #print('オーダー数:%s' % (len(self.dict1.keys())))
        for f in self.dict1.keys():
            v=self.p.get_order(self.pair,f)
            if v['status']=='CANCELED_UNFILLED':
                self.dict1.pop(f)
                sub =('キャンセル： side:%s price:%s amount:%s' % (v['side'],v['price'],v['start_amount']))
                #line.send(co['line_notify_token'],sub)
                print(sub)
                break
            if v['status']=='FULLY_FILLED':
                sub='約定成立： side:%s price:%s amount:%s' % (v['side'],v['price'],v['executed_amount'])
                body=''.join(json.dumps(v))
                m.message_send(sub,body)
                self.dict1.pop(f)
                line.send(co['line_notify_token'],sub)
                print(sub)
                break
            if v['status']=='PARTIALLY_FILLED' and self.dict1[f]==f:
                sub='一部約定成立：side:%s price:%s amount:%s' % (v['side'],v['price'],v['executed_amount'])
                body=''.join(json.dumps(v))
                m.message_send(sub,body)
                line.send(co['line_notify_token'],sub)
                self.dict1[f]="@";
                print(sub)
                break

class mail:
    user = ''
    pas = ''
    to = ''
    def __init__(self,x,y,z):
        self.user = x
        self.pas = y
        self.to = z
    def message_send(self,subject,body):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] =self.user
        msg['To'] = self.to
        msg['Bcc'] = ''
        msg['Date'] = formatdate()
        smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpobj.ehlo()
        smtpobj.starttls()
        smtpobj.ehlo()
        smtpobj.login(self.user, self.pas)
        smtpobj.sendmail(self.user, self.to, msg.as_string())
        smtpobj.close()

class line(object):
    """docstring for line."""
    line_notify_api = 'https://notify-api.line.me/api/notify'
    def send(self,token,msg):
        payload = {'message': msg}
        headers = {'Authorization': 'Bearer ' + token}  # 発行したトークン
        line_notify = requests.post(self.line_notify_api, data=payload, headers=headers)

#main
if __name__ == '__main__':
    conf=open('config.json','r')
    con=json.load(conf)
    co=con['BITBANK']

    API_KEY = co['API_KEY']
    API_SECRET = co['API_SECRET']

    os.system('clear')
    m=mail(co['gmail_add'],co['gmail_pass'],co['to_addr'])
    line=line()
    prv = python_bitbankcc.private(API_KEY, API_SECRET)
    print('start wacth tarde')

    while 1:
        o=orders(prv,'xrp_jpy')
        o.getNewList()
        o.CheckList()
        #o.testsend()
        sleep(2)
