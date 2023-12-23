import pickle
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier 
from sklearn.model_selection import train_test_split

#Abrindo os dados gerados em "post_processing.py"
data_dict = pickle.load(open('./data.pickle', 'rb'))

data = np.asarray(data_dict['data'])
labels = np.asarray(data_dict['labels'])

#Dividindo os dados para teste e para treino
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

#Treinando o modelo
model = MLPClassifier(
    hidden_layer_sizes=(50,),
    activation='relu',
    max_iter = 500

)
model.fit(x_train, y_train)

#Fazendo teste para conferir a precisão do modelo
y_predict = model.predict(x_test)

score = accuracy_score(y_test, y_predict)

print(f'Precisao do modelo = {score*100}%')

#Salvando o modelo treinado para uso
f = open('model.p', 'wb')
pickle.dump({'model': model}, f)
f.close()

