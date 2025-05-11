import re
from flask import jsonify
import requests as req
from bs4 import BeautifulSoup

def check_invoice(target: str,period: str):
    """
    檢查統一發票號碼是否中獎
    :param target: 發票號碼（8 碼數字）
    :param period: 發票期別（index || lastNumber）
    :return Tuple[str, str] 例如 ("中獎", "200萬") 或 ("未中獎", "")
    """
    if len(target) != 8 or not target.isdigit():
        return "格式錯誤", ""

    try:
        print(f"發票號碼: {target} 期別: {period}")
        web = req.get(f'https://invoice.etax.nat.gov.tw/{period}.html')
        web.encoding = 'utf-8'
        soup = BeautifulSoup(web.text, "html.parser")

        td = soup.select('.container-fluid')[0].select('.etw-tbiggest')

        # ✅ 頭獎（從容易中獎的開始比）
        n2 = [td[2].getText()[-8:], td[3].getText()[-8:], td[4].getText()[-8:]]
        n2 = ["12345678","12347891","44244767"]
        for num in n2:

            if target == num:
                return "中獎！ ", "20萬元"
            elif target[-7:] == num[-7:]:
                return "中獎！ ", "4萬元"
            elif target[-6:] == num[-6:]:
                return "中獎！ ", "1萬元"
            elif target[-5:] == num[-5:]:
                return "中獎！ ", "4千元"
            elif target[-4:] == num[-4:]:
                return "中獎！ ", "1千元"
            elif target[-3:] == num[-3:]:
                return "中獎！ ", "2百元"

        # ✅ 特獎
        n1 = td[1].getText()[-8:]
        if target == n1:
            return "中獎！ ", "200萬"

        # ✅ 特別獎
        ns = td[0].getText()[-8:]
        if target == ns:
            return "中獎！ ", "1000萬"

        return "未中獎！ ", ""

    except Exception as e:
        return "系統錯誤", str(e)

def get_period():
    """
    獲取統一發票號碼月份
    :return: str
    """
    try:
        web = req.get(f'https://invoice.etax.nat.gov.tw/index.html')
        web.encoding = 'utf-8'
        soup = BeautifulSoup(web.text, "html.parser")

        # 尋找中獎號碼單的連結文字
        items = soup.select('.etw-web .etw-submenu01 li a')

        # 使用正則過濾中獎號碼單，並擷取月份文字
        pattern = re.compile(r'(\d{3}年\d{2}-\d{2}月)中獎號碼單')

        periods = []
        for item in items:
            match = pattern.search(item.get('title',''))
            if match:
                periods.append(match.group(1))

        return periods

    except Exception as e:
        return "invoice_period.py: ", str(e)

def get_number(period: str):
    """
    獲取統一發票中獎號碼
    :param period: 發票期別（index || lastNumber）
    :return
    """
    # 統一發票號碼獎中獎號碼 入口網站
    web = req.get(f'https://invoice.etax.nat.gov.tw/{period}.html')
    web.encoding = 'utf-8'

    # 使用 Beautiful Soup 解析資料
    soup = BeautifulSoup(web.text, "html.parser")
    time_now_period = soup.select('.etw-web ul li')[0].getText()
    time_now_period = time_now_period.split("中獎號碼單")[0]
    time_last_period = soup.select('.etw-web ul li')[2].getText()
    time_last_period = time_last_period.split("中獎號碼單")[0]

    td = soup.select('.container-fluid')[0].select('.etw-tbiggest')  # 取出中獎號碼的位置
    ns = td[0].getText()  # 特別獎
    n1 = td[1].getText()  # 特獎
    # 頭獎，因為存入串列會出現 /n 換行符，使用 [-8:] 取出最後八碼
    n2 = [td[2].getText()[-8:], td[3].getText()[-8:], td[4].getText()[-8:]]

    return jsonify({
        'now' : time_now_period,
        'last' : time_last_period,
        'ns' : ns,
        'n1' : n1,
        'n2' : n2,
    })