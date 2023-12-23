#Programa para identificar os landmarks nas imagens coleteadas
#Gera um arquivo com os arrays das posições dos landmarks

import os
import mediapipe as mp
import cv2
import pickle

#Define a pasta com as imagens a serem processadas
DATA_DIR = './data'

#Preparando o hands landmark detection do mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.5)

#Iterações para processar cada imagem de cada pasta na pasta data
#Assim, processando as imagens de todas as letras
data = []
labels = []
for dir_ in os.listdir(DATA_DIR):
    for img_path in os.listdir(os.path.join(DATA_DIR, dir_)):
        data_aux = []

        x_ = []
        y_ = []

        img = cv2.imread(os.path.join(DATA_DIR, dir_, img_path))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #processando a imagem com o Hands Landmark Detector do mediapipe
        results = hands.process(img_rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y

                    x_.append(x)
                    y_.append(y)

                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    data_aux.append(x - min(x_))
                    data_aux.append(y - min(y_))
            #Salvando os pontos/landmarks definidos na foto processada
            data.append(data_aux)
            labels.append(dir_)

#Gerando um arquivo para salvar os dados processados
f = open('data.pickle', 'wb')
pickle.dump({'data': data, 'labels': labels}, f)
f.close()

