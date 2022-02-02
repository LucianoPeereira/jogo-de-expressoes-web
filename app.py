from email import message
import uvicorn
import asyncio
import time
import base64
import numpy as np
import cv2
from io import BytesIO
from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from camera import Camera

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/templates", StaticFiles(directory="templates", html=True), name="templates")

def convert_image_to_jpeg(image):
    frame = cv2.imencode('.jpg', image)[1].tobytes()
    frame = base64.b64encode(frame).decode('utf-8')
    return "data:image/jpeg;base64,{}".format(frame)

def cap_vid(camera):
    frame = camera.get_video()
    return frame

def cap(camera):
    frame = camera.get_video()
    exp = camera.get_exp(frame) 
    return str(exp), frame

def time_as_int():
    return int(round(time.time() * 100))  

@app.get('/')
async def index(request: Request):
    return templates.TemplateResponse('client.html', {"request": request})

@app.websocket("/emo")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()  
    
    while True:
        data = await websocket.receive_text()
        if data == 'go':
            # current_time = 0
            # start_time = time_as_int()
            # while current_time <= 500:
            #     current_time = time_as_int() - start_time

            #     emo_mestre,frame = cap(Camera())
            #     result = {
            #         "message": "mestre",
            #         "imagem": convert_image_to_jpeg(frame),
            #         "emocao": emo_mestre
            #     }
            #     await websocket.send_json(result) 
            #     await asyncio.sleep(0.001)
            emo_mestre,frame = cap(Camera())
            result = {
                    "message": "mestre",
                    "imagem": convert_image_to_jpeg(frame),
                    "emocao": emo_mestre
                }
            await websocket.send_json(result) 
            
            

            emo_aluno, frame = cap(Camera())
            result = {
                "message": "aluno",
                "imagem": convert_image_to_jpeg(frame),
                "emocao": emo_aluno
            }
            await websocket.send_json(result) 
            if emo_mestre == emo_aluno:
                result_comp = {
                    "message": "resposta",
                    "result": True 
                }
                await websocket.send_json(result_comp) 
            else: 
                result_comp = {
                    "message": "resposta",
                    "result": False 
                }
                await websocket.send_json(result_comp) 
                                        
               
                
        elif data == 'stop': 
            break
        
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)