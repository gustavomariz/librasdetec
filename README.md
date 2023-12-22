# Detector de Sinais de LIBRAS

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

O MediaPipe é uma estrutura de código aberto desenvolvida pelo Google, usada para processamento de mídia em tempo real, incluindo análise de vídeo, reconhecimento facial, detecção de objetos e muito mais. Ele oferece várias soluções pré-construídas, incluindo o módulo Hand Tracking (rastreamento de mãos), que fornece informações detalhadas sobre a localização e movimento das mãos em tempo real.

O MediaPipe Hand Landmarks utiliza uma arquitetura de rede neural convolucional (CNN) para realizar o rastreamento preciso dos pontos da mão em tempo real. Esta CNN é treinada usando uma técnica chamada "supervisão fraca", na qual grandes quantidades de dados de mãos em diferentes poses são alimentadas à rede (mais de 30.000 imagens), permitindo que ela aprenda padrões visuais associados a esses pontos-chave.

No treinamento, a rede é exposta a imagens rotuladas, onde cada ponto da mão (articulações dos dedos, base da palma, centro da mão) é identificado. A CNN aprende a extrair características importantes dessas imagens para identificar esses pontos com precisão.

Durante a inferência em tempo real, quando um vídeo ou imagem é passado para o modelo, a CNN realiza uma série de operações matriciais e convoluções para identificar características distintivas que representam os pontos específicos da mão. Isso pode incluir a detecção de bordas, padrões de textura e formas que são consistentes com dedos, palma e outras partes da mão.

O modelo é projetado para ser eficiente e rápido, permitindo que o MediaPipe processe cada quadro de vídeo em tempo real, identificando e rastreando os pontos da mão à medida que ela se move. Isso é essencial para aplicações que exigem interações em tempo real, como controle gestual em jogos, realidade aumentada ou interfaces de usuário baseadas em gestos.

Os pontos detectados são então traduzidos em coordenadas espaciais, fornecendo informações sobre a posição tridimensional dos marcos da mão. Esses dados são disponibilizados para os desenvolvedores, permitindo que eles criem interações personalizadas em seus aplicativos com base nos movimentos e gestos da mão.
