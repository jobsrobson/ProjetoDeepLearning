# Redimensiona imagens organizadas em subpastas por classe para 299x299 pixels,
# mantendo a estrutura de pastas na pasta de destino.

from PIL import Image
import os

def redimensionar_imagens_com_subpastas(pasta_raiz_origem, pasta_raiz_destino, novo_tamanho=(299, 299)):
    """
    Redimensiona imagens organizadas em subpastas por classe, mantendo
    a estrutura de pastas na pasta de destino.

    Args:
        pasta_raiz_origem (str): Caminho para a pasta raiz que contém as subpastas das classes.
        pasta_raiz_destino (str): Caminho para a pasta raiz onde as imagens redimensionadas
                                   e as subpastas serão salvas.
        novo_tamanho (tuple): Uma tupla (largura, altura) para o novo tamanho da imagem.
    """
    if not os.path.exists(pasta_raiz_destino):
        os.makedirs(pasta_raiz_destino)
        print(f"Criada pasta de destino principal: {pasta_raiz_destino}")

    # Percorre os itens (subpastas de classes) dentro da pasta raiz de origem
    for class_name in os.listdir(pasta_raiz_origem):
        class_origem_path = os.path.join(pasta_raiz_origem, class_name)
        class_destino_path = os.path.join(pasta_raiz_destino, class_name)

        # Verifica se o item é um diretório (ou seja, uma pasta de classe de resistor)
        if os.path.isdir(class_origem_path):
            # Cria a subpasta correspondente no diretório de destino, se ela não existir
            if not os.path.exists(class_destino_path):
                os.makedirs(class_destino_path)
                print(f"  Criada subpasta de destino para classe: {class_name}")

            print(f"Processando imagens na classe: {class_name}")

            # Agora, percorre os arquivos dentro desta subpasta de classe
            for filename in os.listdir(class_origem_path):
                # Verifica se o arquivo é uma imagem
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    filepath_origem = os.path.join(class_origem_path, filename)
                    filepath_destino = os.path.join(class_destino_path, filename)

                    try:
                        with Image.open(filepath_origem) as img:
                            # Redimensiona a imagem usando o algoritmo Lanczos para alta qualidade
                            img_redimensionada = img.resize(novo_tamanho, Image.Resampling.LANCZOS)
                            img_redimensionada.save(filepath_destino)
                    except Exception as e:
                        print(f"    Erro ao processar {filename} na classe {class_name}: {e}")

    print("\nProcessamento concluído!")

pasta_raiz_origem = '/home/guiro/Documents/Faculdade/Deep_Learning/1'
pasta_raiz_destino = '/home/guiro/Documents/Faculdade/Deep_Learning/resistore_299'


redimensionar_imagens_com_subpastas(pasta_raiz_origem, pasta_raiz_destino)

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Normalizar os pixels

from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Normalização de pixel (0-255 → 0-1)
datagen = ImageDataGenerator(rescale=1./255)

# Carrega imagens a partir de diretórios estruturados por classe
train_generator = datagen.flow_from_directory(
    pasta_raiz_destino,
    target_size=(299, 299),   # Ou o tamanho que você escolheu
    batch_size=32,
    class_mode='categorical'  # ou 'sparse' se estiver usando rótulos inteiros
)


import tensorflow as tf
from tensorflow.keras import layers, models

# Diretório onde estão suas imagens organizadas por pasta/classe
path_imagens = pasta_raiz_destino

# Geradores com normalização (0-1) e divisão de treino/validação
datagen = ImageDataGenerator(
    rescale=1./255,
)

# Conjuntos de treino e validação
train_generator = datagen.flow_from_directory(
    path_imagens,
    target_size=(299, 299),
    batch_size=32,
    class_mode='categorical',
    subset='training'
)

# Número de classes (etiquetas/pastas)
num_classes = train_generator.num_classes

# Modelo CNN simples
model = models.Sequential([
    tf.keras.Input(shape=(299, 299, 3)),
    layers.Conv2D(32, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),  # Adicione mais pooling para reduzir
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(num_classes, activation='softmax')
])

# Compilar modelo
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Treinamento
history = model.fit(
    train_generator,
    epochs=10
)