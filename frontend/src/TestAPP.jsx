import React, { useRef, useState, useEffect } from "react";
import "./App.css";

const TestApp = () => {
    const videoRef = useRef(null); 
    const startCamera = () => {
        navigator.mediaDevices
        .getUserMedia({ video: { facingMode: "environment" } })
        .then((s) => {
            if (videoRef.current) {
                videoRef.current.srcObject = s;
            }
        })
    }
    return (
    <>
        <button onClick={startCamera}>打開相機</button>
        <video ref={videoRef} autoPlay playsInline></video>
     </>
     )
}; 

export default TestApp