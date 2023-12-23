
# Detector de Sinais de LIBRAS


![libras-1024x585](https://github.com/gustavomariz/librasdetec/assets/82617621/62197e5c-79c2-4778-a73a-63bfd5b218b9)


## Objetivo


Esse projeto tem como objetivo final desenvolver um programa que, à partir de uma câmera ao vivo, seja capaz de detectar os gestos da mão do usuário e identificar o sinal específico que está sendo realizado. Para esse projeto final de disciplina em específico, limitei o programa à identificação de dígitos do alfabeto em LIBRAS, desconsiderando aqueles que exigem, além de um símbolo com as mãos, um movimento.

## Abordagem Escolhida

Ao iniciar o desenvolvimento do projeto pesquisei em diversas fontes sobre como é abordado o reconhecimento de gestos, para qualquer que seja a finalidade. Durante essa pesquisa, reconheci três principais abordagens:

- Treinamento em cima da imagem como um todo:

    Nesse caso seriam colhidas imagens de pessoas realizando os gestos a serem treinados. Assim, o classificador escolhido seria treinado a partir dessas fotos para identificar os sinais. Tal abordagem tem diversas dificuldades que envolvem a composição das imagens de treinamento, que além de ser um dado relativamente grande, podem conter "ruídos" como fundos da imagem diferentes, pessoas diferentes realizando os sinais, entre outros. Com isso seria necessária uma base de dados extensa e um classificador robusto.

- Treinamento à partir de um recorte da mão

    Com essa abordagem temos o dado um pouco mais simplificado do que no anterior, em que ao invés da foto por completo, teríamos um recorte que isola as mãos. Porém, ainda sofremos com problemas parecidos, em que podemos ter variações no fundo da foto, na cor da pele, entre outras. Além disso, pensando em usar a câmera para reconhecimento ao vivo, o recorte da mão ficava cada vez mais complicado, limitando o programa.

- Treinamento à partir da posição de landmarks na mão

    Depois de muita pesquisa e algumas frustrações em relação às outras abordagens, fui introduzido ao Mediapipe, API desenvolvida pelo Google para facilitar tarefas de visão computacional, oferecendo uma extensa biblioteca. Dentro do Mediapipe conheci o Hand Landmarks Detection, que me permitiu realizar um tracking da mão e de pontos críticos dela (landmarks). Assim, tive a oportunidade de treinar o classificador por meio da posição desses landmarks, o que pemite que um treinamento feito por algumas imagens minhas seja suficiente para reconhecer outras pessoas em outros cenários fazendo sinais.

Assim escolhi utilizar o Mediapipe, que além de simplificar o programa, na minha visão o deixou mais interessante, justamente pelo live tracking.

## Sobre o Mediapipe

![hand_crops](https://github.com/gustavomariz/librasdetec/assets/82617621/2b948af5-4068-4308-a911-b7dca352cdfb)


O MediaPipe é uma estrutura de código aberto desenvolvida pelo Google, usada para processamento de mídia em tempo real, incluindo análise de vídeo, reconhecimento facial, detecção de objetos e muito mais. Ele oferece várias soluções pré-construídas, incluindo o módulo Hand Tracking (rastreamento de mãos), que fornece informações detalhadas sobre a localização e movimento das mãos em tempo real.

O MediaPipe Hand Landmarks utiliza uma arquitetura de rede neural convolucional (CNN) para realizar o rastreamento preciso dos pontos da mão em tempo real. Esta CNN é treinada usando uma técnica chamada "supervisão fraca", na qual grandes quantidades de dados de mãos em diferentes poses são alimentadas à rede (mais de 30.000 imagens), permitindo que ela aprenda padrões visuais associados a esses pontos-chave.

No treinamento, a rede é exposta a imagens rotuladas, onde cada ponto da mão (articulações dos dedos, base da palma, centro da mão) é identificado. A CNN aprende a extrair características importantes dessas imagens para identificar esses pontos com precisão.

Durante a inferência em tempo real, quando um vídeo ou imagem é passado para o modelo, a CNN realiza uma série de operações matriciais e convoluções para identificar características distintivas que representam os pontos específicos da mão. Isso pode incluir a detecção de bordas, padrões de textura e formas que são consistentes com dedos, palma e outras partes da mão.

O modelo é projetado para ser eficiente e rápido, permitindo que o MediaPipe processe cada quadro de vídeo em tempo real, identificando e rastreando os pontos da mão à medida que ela se move, algo essencial para cumprir o objetivo desse projeto. 

Os pontos detectados são então traduzidos em coordenadas espaciais, fornecendo informações sobre a posição tridimensional dos marcos da mão. Tal tradução me perimitiu simplificar os dados relativos às fotos ou ao vídeo ao vivo, os quais se tornaram, como dito anteriormente, apenas linhas com um label e a posição dos pontos. 

Caso se interesse mais pela ferramenta e quiser testar você mesmo, segue o link para um teste web do Mediapipe Hands Landmarks Detector: https://developers.google.com/mediapipe/solutions/vision/gesture_recognizer

## Coleta e Processamento dos Dados

Com a abordagem escolhida e o Mediapipe estudado, podemos seguir para o desenvolvimento.

Para a coleta dos dados, desenvolvi o programa coleta_img.py para tirar 100 fotos minhas fazendo cada um dos sinais, tentando variar um pouco a posição da mão no frame da foto enquanto realizo a captura das fotos de um sinal. Assim foi gerada uma base com 2000 fotos, considerando que nesse projeto vou tentar identificar apenas 20 dígitos, excluindo os que têm sinais com movimento.

Com essa base criada, vamos processar essas imagens com o Mediapipe por meio do programa processa_img.py. Nele, cada imagem é processada pelo Hands Landmarks Detection de forma que ele encontra cada landmark da mão na foto e retorna a posição desses pontos (x e y). Assim, cria-se uma nova base de dados, que ao invés de fotos, tem para cada linha coordenadas de pontos e um label, que no caso, é um id referente a letra feita no sinal da foto.

Finalmente, por meio da biblioteca pickle, é gerado um arquivo dessa base de dados para a leitura posterior.
 
## Treinamento

<img width="598" alt="Sklearn-Neural-Network-MLPRegressor-Regression-Model-" src="https://github.com/gustavomariz/librasdetec/assets/82617621/2a261f58-76f6-4ec5-b49a-069c1cc6dcce">

Para o treinamento e classificação, quis trabalhar nesse projeto com redes neurais simples e, para isso, utilizei a biblioteca scikit-learn e sua implementação de um Multi-Layer Perceptron.

o Multi-Layer Perceptron (MLP) Classifier é composto por várias camadas de neurônios, incluindo uma camada de entrada, uma ou mais camadas ocultas e uma camada de saída.

A matemática por trás do MLP envolve uma série de operações, incluindo:

- Camada de Entrada:

    Cada neurônio na camada de entrada recebe um valor de entrada. Esses valores são os recursos ou características do conjunto de dados. Cada recurso é multiplicado por um peso correspondente.
  
- Camadas Ocultas:

    Cada camada oculta é composta por neurônios que recebem os valores dos neurônios da camada anterior. Cada conexão entre neurônios tem um peso associado.
Para calcular a saída de um neurônio na camada oculta, os valores de entrada são ponderados pelos pesos e somados. Essa soma é então passada por uma função de ativação, como a função sigmoide, tangente hiperbólica ou ReLU (Rectified Linear Unit).
A função de ativação introduz não linearidade na rede, permitindo que ela aprenda relações complexas nos dados.

- Camada de Saída:

    Os valores calculados nas camadas ocultas são propagados para a camada de saída. Esta camada produz as previsões finais.
A ativação na camada de saída pode variar dependendo do tipo de problema: uma função sigmoide é comumente usada para classificação binária, uma função softmax para classificação multiclasse e nenhuma ativação para regressão.
    
Durante o treinamento, a rede passa pelos seguintes passos:

- Inicialização dos Pesos:

    Os pesos da rede são inicializados aleatoriamente.
  
- Feedforward (Propagação Direta):

    Os dados de entrada são alimentados pela rede, passando por cada camada até a camada de saída. As saídas são calculadas usando os pesos e as funções de ativação.
  
- Cálculo do Erro:

    A diferença entre as previsões da rede e os rótulos reais do conjunto de treinamento é calculada usando uma função de custo, como a função de erro quadrático médio ou a entropia cruzada.
  
- Backpropagation:

    O algoritmo de backpropagation ajusta os pesos da rede para minimizar o erro calculado.
    Os gradientes do erro em relação aos pesos são calculados usando o gradiente descendente, atualizando os pesos para reduzir gradualmente o erro.
  
- Atualização dos Pesos:

    Os pesos são atualizados iterativamente usando otimizadores, como o Gradiente Descendente Estocástico (SGD) com uma taxa de aprendizado.
    Este processo é repetido por várias iterações até que a rede neural alcance uma boa performance nos dados de treinamento ou atinja o número máximo de iterações estipulado.

Para o programa em questão, fiz testes com diferentes parâmetros do MLPClassifier e cheguei numa construção bem simples da rede que é mais do que suficiente para atender a classificação desejada.
No caso a rede construída tem apenas uma camada oculta com 50 nós, e um número máximo de iterações de 500. Além disso, foi escolhida a função de ativação "relu". 
Ela é uma função simples e eficaz que retorna zero para valores negativos e o próprio valor para valores positivos. Apesar da sua simplicidade, sua natureza de ativação não-linear já é suficiente para a rede aprender relações complexas nos dados.
Os outros parâmetro relativos ao cálculo do erro, sua tolerância e ao cálculo do gradiente descendente são os já predefinidos pela biblioteca, se quiser conferir exatamente acesse aqui: https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html

Assim separei os dados em dados de treino e dados de teste (20% das imagens foram separadas para teste). Após realizar o treino, foi identificada uma precisão de 100% (pode haver um overfitting, pelo problema ser bem simples, mas nos testes práticos o programa funciona bem).

Por fim, salvei o modelo treinado no arquivo model.p para a posterior leitura.

## Aplicatvo

O desenvolvimento do aplicativo foi bem simples, apenas utilizei a biblioteca opencv para abrir a janela com a câmera ao vivo, de forma que o Mediapipe recebe os frames da câmera e já forma os pontos e suas posições.
 Assim fui capaz de desenhar esses pontos na imagem, para ilustração e para identificar quando a mão está de fato sendo reconhecida corretamente. Com esses dados do Mediapipe sendo gerados a cada frame, eles passam pelo modelo treinado que identifica qual a letra referente ao sinal que está sendo feito, o que trouxe um resultado bem satisfatório.

 Segue um vídeo com o aplicativo em funcionamento:

 
