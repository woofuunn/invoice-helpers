import React, { useRef, useState, useEffect } from "react";
import "./App.css";
import Tesseract from "tesseract.js";

const App = () => {
  const videoRef = useRef(null);
  const [stream, setStream] = useState(null);
  const [captureInterval, setCaptureInterval] = useState(null);
  const [resultText, setResultText] = useState({ result: "", number: "" });
  const resultTextRef = useRef("");
  const [invoiceNumberData, setinvoiceNumberData] = useState(null);
  const [isCameraActive, setCameraActive] = useState(false);
  const [selectedPeriod, setSelectedPeriod] = useState("index");
  const selectedPeriodRef = useRef(selectedPeriod);
  const [selectedContainer, setSelectedContainer] = useState("winners");
  const isRecognizingRef = useRef(false);
  const [recognizingText, setRecognizingText] = useState("");
  // const [isRecognizingState, setIsRecognizingState] = useState(false);

  //// 測試用 (Line打開網頁時，自動導向瀏覽器)
  const isLineBrowser = () => {
    return navigator.userAgent.toLowerCase().indexOf("line") != -1;
  };
  useEffect(() => {
    if (isLineBrowser()) {
      const currentUrl = window.location.href;

      if (navigator.userAgent.toLowerCase().includes("android")) {
        window.location.href = `intent://${currentUrl.replace(
          /^https?:\/\//,
          ""
        )}#Intent;scheme=https;package=com.android.chrome;end`;
      }
    }
  }, []);
  ////

  const startCamera = () => {
    navigator.vibrate(1000);
    setSelectedContainer("helpers");
    setCameraActive(true);

    navigator.mediaDevices
      .getUserMedia({ video: { facingMode: "environment" } })
      .then((s) => {
        if (videoRef.current) {
          videoRef.current.srcObject = s;
          setStream(s);

          setResultText({ result: "", number: "" });

          const captureAndRecognize = () => {
            if (isRecognizingRef.current) return;
            isRecognizingRef.current = true;

            const video = videoRef.current;
            const videoWidth = video.videoWidth;
            const videoHeight = video.videoHeight;

            const canvas = document.createElement("canvas");
            canvas.width = videoWidth;
            canvas.height = videoHeight;

            const ctx = canvas.getContext("2d");

            // 裁切識別區
            const rectWidth = videoWidth * 0.6;
            const rectHeight = 70;
            const rectX = (videoWidth - rectWidth) / 2;
            const rectY = (videoHeight - rectHeight) / 2;
            ctx.drawImage(
              video,
              rectX,
              rectY,
              rectWidth,
              rectHeight,
              0,
              0,
              rectWidth,
              rectHeight
            );

            
            if (resultTextRef.current === "") {
              Tesseract.recognize(canvas, "eng+chi_tra", {}).then(
                ({ data: { text } }) => {
                  const match = text.match(/\d{8}/);
                  if (match) {
                    checkInvoiceNum(match[0]);
                    resultTextRef.current = match[0];
                  }
                  isRecognizingRef.current = false;
                }
              );
            }
            

            
          };

          const interval = setInterval(captureAndRecognize, 1500);
          setCaptureInterval(interval);
        }
      })
      .catch((err) => {
        if (isLineBrowser()) {
          alert("請使用手機瀏覽器開啟，Line內建瀏覽器不支援相機功能！");
        } else {
          alert("相機開啟失敗。");
        }
        // console.log(err)
        setCameraActive(false);
        setSelectedContainer("winners");
      });
  };

  const stopCamera = () => {
    // 停止定時截圖
    if (captureInterval) {
      clearInterval(captureInterval);
      setCaptureInterval(null);
    }

    // 停止相機串流
    if (stream) {
      stream.getTracks().forEach((track) => {
        if (track.readyState === "live") {
          track.stop();
        }
      });
      setStream(null);
    }

    // 清空 OCR 結果與 UI 狀態
    isRecognizingRef.current = false;
    // setIsRecognizingState(false);
    setResultText({ result: "", number: "" });
    resultTextRef.current = "";
    setCameraActive(false);
    setSelectedContainer("winners");

    // 清除畫面上相機畫面
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
  };

  const continueCamera = () => {
    setResultText({ result: "", number: "" });
    resultTextRef.current = "";
    isRecognizingRef.current = "";
    // setIsRecognizingState(true);
  };

  const getInvoiceNumber = (period) => {
    setSelectedPeriod(period);
    fetch(`/api/get_invoice_number?period=${period}`, {
      method: "GET",
    })
      .then((res) => res.json())
      .then((data) => setinvoiceNumberData(data));
  };

  const checkInvoiceNum = (invoiceNum) => {
    fetch("/api/check_invoice_number", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        number: invoiceNum,
        period: selectedPeriodRef.current,
      }),
    })
      .then((res) => res.json())
      .then((data) =>
        setResultText({
          result: data.checkResult,
          number: invoiceNum,
        })
      );
  };

  useEffect(() => {
    getInvoiceNumber(selectedPeriod);
    selectedPeriodRef.current = selectedPeriod;
  }, [selectedPeriod]);

  useEffect(() => {
    let interval = null;

    if (resultText.result === "") {
      let count = 0;
      interval = setInterval(() => {
        count = (count + 1) % 4;
        setRecognizingText("辨識中" + ".".repeat(count));
      }, 800);
    } else {
      setRecognizingText("辨識完成");
    }

    return () => clearInterval(interval);
  }, [resultText]);

  return (
    <>
      <div className="nav">
        <span className="font-weight-bold">對獎小幫手</span>
      </div>

      <div className="component">
        <div className="public">
          {invoiceNumberData && (
            <div className="invoicePeriod">
              <ul>
                <li className={selectedPeriod === "index" ? "selected" : ""}>
                  <button
                    id="invoiceBtn"
                    onClick={() => getInvoiceNumber("index")}
                  >
                    {invoiceNumberData.now}
                  </button>
                </li>
                <li
                  className={selectedPeriod === "lastNumber" ? "selected" : ""}
                >
                  <button
                    id="invoiceBtn"
                    onClick={() => getInvoiceNumber("lastNumber")}
                  >
                    {invoiceNumberData.last}
                  </button>
                </li>
              </ul>
            </div>
          )}
        </div>
        <div className="main">
          {selectedContainer === "winners" && (
            <div className="container-winners">
              {invoiceNumberData && (
                <>
                  <table className="invoiceNum">
                    <thead>
                      <tr>
                        <th width={100}>獎別</th>
                        <th>中獎號碼</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>特別獎</td>
                        <td>
                          <span className="font-weight-bold text-color-red">
                            {invoiceNumberData.ns}
                          </span>
                        </td>
                      </tr>
                      <tr>
                        <td>特獎</td>
                        <td>
                          <span className="font-weight-bold text-color-red">
                            {invoiceNumberData.n1}
                          </span>
                        </td>
                      </tr>
                      {invoiceNumberData.n2.map((n, i) => (
                        <tr key={i}>
                          <td>頭獎</td>
                          <td>
                            <span className="font-weight-bold">
                              {n[0]}
                              {n[1]}
                              {n[2]}
                              {n[3]}
                              {n[4]}
                            </span>
                            <span className="font-weight-bold text-color-red">
                              {n[5]}
                              {n[6]}
                              {n[7]}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </>
              )}
            </div>
          )}
          {selectedContainer === "helpers" && (
            <div className="container-helpers">
              {isCameraActive && (
                <div
                  className={`video-wrapper ${
                    !videoRef.current ? "videoUnready" : ""
                  } `}
                >
                  <div className="video-crop">
                    {resultText.result && (
                      <div className="video-overlay-result">
                        <div id="invoice-result">
                          <p>
                            <span className="result-text">
                              {resultText.result}
                            </span>
                          </p>
                          <p>
                            <span className="result-text">
                              {resultText.number}
                            </span>
                          </p>
                        </div>
                      </div>
                    )}
                    <div className="video-overlay-text">
                      將視窗移至發票號碼上
                    </div>
                    <div className="video-overlay-rect"></div>

                    <div className="video-overlay-status">
                      {recognizingText}
                    </div>

                    <video ref={videoRef} autoPlay playsInline />

                    <div className="video-overlay-button">
                      {isCameraActive && (
                        <>
                          <div className="video-btn-group">
                            <button className="video-btn" onClick={stopCamera}>
                              關閉
                            </button>
                            <button
                              className={`video-btn ${
                                resultTextRef.current === "" ? "hide" : ""
                              }`}
                              onClick={continueCamera}
                            >
                              繼續
                            </button>
                          </div>
                        </>
                      )}
                    </div>
                    <div className="video-mask">
                      <div className="mask mask-top"></div>
                      <div className="mask mask-bottom"></div>
                      <div className="mask mask-left"></div>
                      <div className="mask mask-right"></div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      <div className="footer">
        {!isCameraActive && (
          <div>
            <button className="open-camera-btn" onClick={startCamera}>
              打開
            </button>
          </div>
        )}
        <div className="text-prompt">
          <span>👍點擊【打開】，開始使用小幫手</span>
        </div>
      </div>
    </>
  );
};

export default App;
