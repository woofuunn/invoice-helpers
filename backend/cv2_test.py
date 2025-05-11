import cv2
import requests as req
from bs4 import BeautifulSoup as bs

if __name__ == '__main__':
    # print(cv2.__version__)
    # tracker = cv2.TrackerCSRT()
    # print(type(tracker))
    # tracker_1 = cv2.TrackerKCF()
    # print(type(tracker_1))

    web = req.get('https://invoice.etax.nat.gov.tw/')
    web.encoding = 'utf-8'

    soup = bs(web.text,"html.parser")
    time = soup.select('.etw-web')[0].select('.etw-on')
    # print(time[0].getText())

    td = soup.select('.container-fluid')[0].select('.etw-tbiggest')  # 取出中獎號碼的位置
    ns = td[0].getText()  # 特別獎
    n1 = td[1].getText()  # 特獎
    # 頭獎，因為存入串列會出現 /n 換行符，使用 [-8:] 取出最後八碼
    n2 = [td[2].getText()[-8:], td[3].getText()[-8:], td[4].getText()[-8:]]
    # print(ns)
    # print(n1)
    # print(n2)

