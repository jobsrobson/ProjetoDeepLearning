# Teste com o modelo salvo

import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.inception_v3 import preprocess_input
import numpy as np
import os

# --- 1. Configuração dos Caminhos ---
# Caminho para o modelo salvo
caminho_modelo_salvo = '/modelo_garbage_inception_v1.keras'
# Caminho para a imagem que você quer testar
caminho_imagem_teste = '/content/caixa.jpg' # Substitua pelo caminho da sua imagem de teste

# --- 2. Carregar o modelo ---
try:
    model = load_model(caminho_modelo_salvo)
    print("✅ Modelo carregado com sucesso!")
except Exception as e:
    print(f"❌ ERRO ao carregar o modelo: {e}")

# --- 3. Carregar e pré-processar a imagem ---
try:
    img = load_img(caminho_imagem_teste, target_size=(299, 299))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) # Adiciona a dimensão do batch
    img_array = preprocess_input(img_array) # Aplica o pré-processamento do InceptionV3

    print(f"✅ Imagem '{caminho_imagem_teste}' carregada e pré-processada com sucesso!")
except FileNotFoundError:
    print(f"❌ ERRO: O arquivo de imagem '{caminho_imagem_teste}' não foi encontrado. Verifique o caminho.")
except Exception as e:
    print(f"❌ ERRO: Ocorreu um problema ao carregar ou pré-processar a imagem: {e}")

# --- 4. Fazer a previsão ---
try:
    predictions = model.predict(img_array)
    print("✅ Previsão realizada com sucesso!")
    # print(predictions) # Descomente para ver os valores brutos das probabilidades
except Exception as e:
    print(f"❌ ERRO ao fazer a previsão: {e}")

# --- 5. Interpretar o resultado (Usar nomes das classes fornecidos) ---
# Lista de nomes das classes fornecida pelo usuário
class_labels = [
    'cardboard',
    'glass',
    'metal',
    'paper',
    'plastic',
    'trash'
]

try:
    # Obter a classe prevista (aquela com a maior probabilidade)
    predicted_class_index = np.argmax(predictions)

    # Verificar se o índice previsto está dentro dos limites da lista de classes
    if predicted_class_index < len(class_labels):
        predicted_class_label = class_labels[predicted_class_index]
        print(f"\nA imagem foi classificada como: **{predicted_class_label}**")
        print(f"Probabilidades por classe: {predictions[0]}") # Mostra as probabilidades para cada classe
    else:
        print(f"\nAVISO: O índice da classe prevista ({predicted_class_index}) está fora dos limites da lista de classes fornecida.")
        print(f"Probabilidades por classe: {predictions[0]}") # Mostra as probabilidades para cada classe


except Exception as e:
    print(f"❌ ERRO ao interpretar o resultado: {e}")