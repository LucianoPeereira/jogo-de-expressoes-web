from email import message
from email.mime import base
import uvicorn
import asyncio
import time
import base64
import numpy as np
import cv2
import uuid
import json
from io import BytesIO
from PIL import Image
from typing import List
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, StreamingResponse

from camera import Camera

app = FastAPI()

def convert_image_to_jpeg(image):
    frame = cv2.imencode('.jpg', image)[1].tobytes()
    frame = base64.b64encode(frame).decode('utf-8')
    return "data:image/jpeg;base64,{}".format(frame)

def convert_b64_to_img(data):
    image = data[data.find(",") + 1 :]
    dec = base64.b64decode(image + "===")
    image = Image.open(BytesIO(dec)).convert("RGB")

    name = f"/data/{str(uuid.uuid4())}.png"
    image.filename = name
    i = np.array(image)
    red = i[:,:,0].copy(); i[:,:,0] = i[:,:,2].copy(); i[:,:,2] = red;
    
    return i

def exp(camera, frame):
    exp = camera.get_exp(frame) 
    return str(exp)

def time_as_int():
    return int(round(time.time() * 100))  

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        if len(self.active_connections) >= 2:
            await websocket.accept()
            await websocket.close(4000)
        else:
            await websocket.accept()
            self.active_connections.append(websocket)
            if len(self.active_connections) == 1:
                await websocket.send_json({
                        "current_player": "mestre"
                    })
            elif len(self.active_connections) == 2:
                await websocket.send_json({
                    "current_player": "aluno",
                })
            else:
                manager.disconnect(self)
            
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

@app.websocket("/emo_ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
                
            img = convert_b64_to_img(data)
                
            emo_mestre = exp(Camera(),img)
            
            result = {
                    "player": "mestre",
                    "teste": "funcionou",
                    # "imagem": convert_image_to_jpeg(frame),
                    "emocao": emo_mestre
            }
            await manager.broadcast(result) 
                                            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except:
        pass
        
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)