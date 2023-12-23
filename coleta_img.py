#Programa para coletar immagens para teste e treino
#Gera 100 imagens para cada sinal de LIBRAS

import os
import cv2
import time

#Define a pasta com as fotos
DATA_DIR = './data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

#Define quantas classes/letras e quantas imagens para cada
num_classes = 21
dataset_size = 100

cap = cv2.VideoCapture(0)
for j in range(num_classes):
    if not os.path.exists(os.path.join(DATA_DIR, str(j))):
        os.makedirs(os.path.join(DATA_DIR, str(j)))

    print('Coletando dados para {}'.format(j))

    done = False
    while True:
        ret, frame = cap.read()
        cv2.putText(frame, 'Aperte Q', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,
                    cv2.LINE_AA)
        cv2.imshow('frame', frame)
        if cv2.waitKey(25) == ord('q'):
            break

    cnt = 0
    while cnt < dataset_size:
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        cv2.waitKey(25)
        cv2.imwrite(os.path.join(DATA_DIR, str(j), '{}.jpg'.format(cnt)), frame)

        cnt += 1

cap.release()
cv2.destroyAllWindows()