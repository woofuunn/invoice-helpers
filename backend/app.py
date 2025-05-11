from flask import Flask, request, jsonify, render_template_string
import pytesseract
import cv2
import numpy as np
import re
import base64
import requests as req
from bs4 import BeautifulSoup
from utils.invoice import check_invoice
from utils.invoice import get_period
from flask_cors import CORS


app = Flask(__name__)
CORS(app)   # 解決跨域連線

# 設定 Tesseract 路徑（依安裝位置）
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

@app.route('/')
def index():
    period = get_period()
    html = open("templates/index.html", encoding="utf-8").read()
    return render_template_string(html, period=period)

@app.route('/api/get_invoice_period', methods=['get'])
def get_period():
    period = get_period()
    return jsonify({"period": period})

@app.route('/api/check_invoice_number', methods=['POST'])
def verify_number():
    data = request.get_json()
    number = data.get('number')
    period = data.get('period')
    check_result = check_invoice(number, period)
    return jsonify({
        'checkResult': check_result
    })

## 後端 OCR 做法
@app.route('/api/process', methods=['POST'])
def process():
    data = request.get_json()
    image_data = data.get('image')
    header, encoded = image_data.split(",", 1)
    img_data = base64.b64decode(encoded)

    period_key = data.get('periodKey')

    # 轉成 OpenCV 圖片
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # 設定 ROI 尺寸
    height, width = img.shape[:2]
    w, h, x, y = width-10, 100, 5, height - 105 # 可根據發票實際大小調整

    # 畫出 ROI 區域（純視覺標記）
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 10)

    # 裁切 ROI 區域進行 OCR
    roi = img[y:y + h, x:x + w]

    # OCR 預處理
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # OCR 版本一 (pytesseract.image_to_data())
    # data = pytesseract.image_to_data(thresh, output_type=pytesseract.Output.DICT)
    # pattern = re.compile(r'\d{8}')
    #
    # result_text = ""
    # for i in range(len(data['text'])):
    #     word = data['text'][i].strip()
    #     print(word, end=" ")
    #     match = pattern.search(word)
    #     if match:
    #         # print(match.group())  ##debug
    #         result, prize = check_invoice(match.group(), period_key)
    #         result_text = f"{match.group()}: {result}! {prize}"
    #         # x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
    #         # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    #         # cv2.putText(img, word, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    #         break  # 只比對找到的第一組號碼

    # OCR 版本二 (pytesseract.image_to_string())
    text = pytesseract.image_to_string(thresh, config='--psm 6')
    print(text)
    # 抓出發票號碼（8 碼）
    match = re.search(r'\d{8}', text)

    result_text = ""
    if match:
        result, prize = check_invoice(match.group(), period_key)
        result_text = f"{match.group()}: {result}! {prize}"

    # 回傳處理後的整張圖（包含原圖＋框）
    img[y:y+h, x:x+w] = roi  # 把修改過的 ROI 放回原圖

    # 回傳影像 base64
    _, buffer = cv2.imencode('.jpg', img)
    processed_base64 = base64.b64encode(buffer).decode('utf-8')
    return jsonify({
        'result' : 'data:image/jpeg;base64,' + processed_base64,
        'checkResult': result_text
    })


@app.route('/api/get_invoice_number', methods=['get'])
def get_number():
    period = request.args.get("period")

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)