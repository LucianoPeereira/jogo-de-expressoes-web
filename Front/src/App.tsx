import { render } from "@testing-library/react";
import React, { useEffect, useRef, useState, useCallback } from "react";
import Webcam from "react-webcam";

function App() {

  const webcamRef = useRef<Webcam>(null);
  const ws = useRef<any>(null);
  const [camMestre, setCamMestre] = useState("block")


  const [capturedImg, setCapturedImg] = useState<any>(null);
  const [prediction, setPrediction] = useState("");
  const [player, setPlayer] = useState("")

  const [isPaused, setPause] = useState(false);

  useEffect(() => {
    const client_id = Date.now();
    const url = `ws://localhost:8000/emo_ws/{`+client_id+`}`;
    console.log(url);
  
    ws.current = new WebSocket(url);
    ws.current.onopen = () => console.log("ws opened");
    ws.current.onclose = () => console.log("ws closed");

    return () => {
      ws.current.close();
    };
  
  
  }, []);

  useEffect(() => {
    if (!ws.current) return;

    ws.current.onmessage = (event: any) => {
      if (isPaused) return;
      const message = JSON.parse(event.data);
      console.log(message);
      if(message.current_player){
        setPlayer(message.current_player)
      }
      setPrediction(message.emocao);
    };
  }, [isPaused]);

  function sendMessage(msg: any) {
    if (!ws.current) return;
    ws.current.send(msg);
  }

  function Greeting(props: any){
    if (capturedImg !== null){
      return <img src={capturedImg} alt="" />
    }
    return <Webcam
              audio={false}
              height={400}
              ref={webcamRef}
              screenshotFormat="image/jpeg"
              width={600}
              videoConstraints={videoConstraints}
            /> 
  }

  const videoConstraints = {
    width: 1280,
    height: 720,
    facingMode: "environment", // Can be "environment" or "user"
  };

  const capture = useCallback(() => {
    if (webcamRef.current) {
      const capturedImg = webcamRef.current.getScreenshot();
      sendMessage(capturedImg);
      setCapturedImg(capturedImg)
    }
  }, [webcamRef]);

  return (
    <div className="">
      <h1>{player}</h1>
      <p>
        <button onClick={capture}>Capture photo</button>
      </p>
      <Greeting /> 
      <h3>{prediction && prediction}</h3>
    </div>
  );
  
}

export default App;