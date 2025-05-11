# 對獎小幫手（Invoice Helper）

## 前言

「對獎小幫手」這個專案的出發點，是希望改善目前市面上對獎 APP 的使用體驗。

多數 App 雖然支援電子發票掃碼，但紙本傳統發票需手動輸入發票末三碼來查詢，使用上稍嫌麻煩。

因此我想設計一個更簡單的對獎工具，透過手機鏡頭辨識發票號碼，自動比對中獎號碼，讓結果即時呈現給使用者。

## 專案簡介

此專案主要是用 Python 來開發，後端採用 Flask 實作 API ，負責處理中獎號碼的比對，並透過 BeautifulSoup 爬蟲取得財政部網站的對獎資訊。

前端則用 React，介面比較靈活，搭配 Tesseract OCR 技術，在手機拍攝中辨識發票號碼。

不同於一般對獎 APP，選擇開發成網頁版本，讓不同作業系統的手機都能使用，以實現跨平台 。
    
    
## 專案結構

```
invoice-helpers/
├── frontend/ # React (於 VS Code 開發)
└── backend/ # Flask-api (於 PyCharm 開發)
```

##  開發與執行方式

### 前端：React
```bash
cd frontend
npm install
npm run dev
```

### 後端：Flask
```bash
cd backend
python -m venv venv
source venv\Scripts\activate #（Windows） ; （Linux / macOS） 用 venv/bin/activate
pip install -r requirements.txt
python app_api.py
```

## 使用技術
- 前端：React
- 後端： Python（Flask RESTful API）
- 圖像辨識：Tesseract OCR
- 資料擷取：Beautiful Soup（爬蟲）
- 測試工具：Ngrok（本機外部連線）
- 開發環境：Visual Studio Code、 PyCharm

## 功能介紹

### 流程大致如下：
1. 預設頁面顯示最新一期中獎號碼
2. 可選擇最新一期或上一期(依財政部網站為準)
3. 開啟相機，前端使用 OCR 辨識發票號碼
4. 後端進行比對中獎獎號 
5. 回傳是否中獎，以及對應獎金.

    
    
