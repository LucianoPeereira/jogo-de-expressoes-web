import cv2
import numpy as np
from rmn import RMN

rmn = RMN()

class Camera():
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()
    
    def get_exp(self):
        ret, frame = self.video.read()
        while self.video.isOpened():
            results = rmn.detect_emotion_for_single_frame(frame)
            for result in results:
                emolabel = result['emo_label']
                
                return self.translateEmo(emolabel), frame
            
    def translateEmo(self,emolabel):  # Traduz o emolabel para o 'OutMestre' da JANELA2
        emocao = ""

        if(emolabel == 'happy'):
            emocao = "Feliz"
        elif(emolabel == 'sad'):
            emocao = "Triste"
        elif(emolabel == 'neutral'):
            emocao = "Neutro"
        elif(emolabel == 'disgust'):
            emocao = "Nojo"
        elif(emolabel == 'fear'):
            emocao = "Medo"
        elif(emolabel == 'angry'):
            emocao = "Bravo"
        elif(emolabel == 'surprise'):
            emocao = "Surpreso"

        return emocao
