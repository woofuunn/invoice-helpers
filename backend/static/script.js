let stream = null;
let captureInterval = null;
const video = document.getElementById("video");
const processedImg = document.getElementById("processed");

function showPage(id) {
    document.querySelectorAll('.page').forEach(div => {
      div.classList.remove('active');
    });
    document.getElementById(id).classList.add('active');
}

function startCamera() {
  navigator.mediaDevices.getUserMedia({
    video: {
        facingMode: "environment",
//        width: { ideal: 640 },  // 或 exact: 640
//        height: { ideal: 480 }
    }
  })
  .then(s => {
    stream = s
    video.srcObject = stream;

    // 每秒擷取畫面並送出
    captureInterval = setInterval(() => {
      const canvas = document.createElement("canvas");
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

      // 當前畫面
      const dataURL = canvas.toDataURL("image/jpeg");

      // 取得目前選取的發票期別（index 或 lastNumber）
      const selectedPeriod = document.querySelector('input[name="invoicePeriod"]:checked').value;

      fetch("api/verify_invoice_number", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            image: dataURL,
//            periodKey: selectedPeriod
            periodKey: 'index'
        })
      })
      .then(res => res.json())
      .then(data => {

        // 影像
        if (data.result) {
          processedImg.src = data.result;
        }

        // 中獎結果
        if(data.checkResult){
            // 顯示結果與按鈕
            document.getElementById('result-text').textContent = data.checkResult;
            document.getElementById('invoice-result').style.display = 'block';
        }
      });
    }, 1000); // 每秒一次

    // 切換按鈕顯示
    document.getElementById("startBtn").style.display = "none";
    document.getElementById("stopBtn").style.display = "inline";
  })
  .catch(err => alert("相機無法啟動：" + err));
}

function closeCamera() {
  if (stream) {
    stream.getTracks().forEach(track => track.stop());
    video.srcObject = null;
    stream = null;
  }

  if (captureInterval) {
    clearInterval(captureInterval);
    captureInterval = null;
  }

  // 切換按鈕顯示
  document.getElementById("startBtn").style.display = "inline";
  document.getElementById("stopBtn").style.display = "none";

  // 可選：重設預設圖片
  processedImg.src = "";
}

function getInvoiceNum(){
    fetch('/api/invoice', {
        method:'post',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ period: 'index'}),
    })
    .then(res => res.json())
    .then(data => {
        if(data){
            const ul = document.querySelector(".etw-web ul");
            ul.innerHTML = `<li>${data.now}</li>`

            const tbody = document.querySelector(".invoiceNum tbody");
            tbody.innerHTML = ""; // 清空舊資料

            const rows = [
                {prize: "特別獎", number: data.ns},
                {prize: "特獎", number: data.n1},
                {prize: "頭獎", number: data.n2[0]},
                {prize: "頭獎", number: data.n2[1]},
                {prize: "頭獎", number: data.n2[2]},
            ];

            // 如果增設六獎
            if(data.n_add != null){
                data.n_add.forEach(n => {
                    rows.push({prize: "增開六獎", number: n});
                });
            }

            rows.forEach(item => {
                const tr = document.createElement("tr");
                tr.innerHTML = `<td>${item.prize}</td><td>${item.number}</td>`;
                tbody.appendChild(tr);
            });

        }
    })
}

function sendImage(base64Image) {
    fetch('/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: base64Image })
    })
    .then(res => res.json())
    .then(data => {
        // 顯示圖片
        document.getElementById('image-preview').innerHTML = `<img src="${data.result}" width="300">`;

        // 顯示結果與按鈕
        document.getElementById('result-text').textContent = data.checkResult;
        document.getElementById('invoice-result').style.display = 'block';
    });
}

function continueScan() {
    document.getElementById('invoice-result').style.display = 'none';
    // 這裡可以清空畫面、清空檔案、重新拍攝等等
}

function closeResult() {
    document.getElementById('invoice-result').style.display = 'none';
    // 額外：你也可以直接關掉 modal 或回到首頁
}