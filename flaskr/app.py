import os
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.inception_v3 import preprocess_input
import numpy as np
from pyngrok import ngrok

# --- Configuração Inicial ---
app = Flask(__name__, template_folder="template")

# Configura o caminho para a pasta de uploads
UPLOAD_FOLDER = 'file_uploaded'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Garante que a pasta de uploads exista
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- 1. Configuração dos Caminhos e Carregamento do Modelo ---
caminho_modelo_salvo = 'flaskr/modelo_garbage_inception_v1.keras'

try:
    model = load_model(caminho_modelo_salvo)
    print("✅ Modelo carregado com sucesso!")
except Exception as e:
    print(f"❌ ERRO ao carregar o modelo: {e}")
    model = None # Garante que o app não quebre se o modelo não carregar

### NOVO: Dicionário para mapear a classe para a cor da lixeira e informações ###
recycling_info_map = {
    'paper': {
        'nome': 'Papel',
        'cor_lixeira': 'Azul',
        'hex_cor': '#007bff',
        'descricao': 'Descarte na lixeira AZUL. Reciclável.'
    },
    'cardboard': {
        'nome': 'Papelão',
        'cor_lixeira': 'Azul',
        'hex_cor': '#007bff',
        'descricao': 'Descarte na lixeira AZUL. Reciclável.'
    },
    'plastic': {
        'nome': 'Plástico',
        'cor_lixeira': 'Vermelho',
        'hex_cor': '#dc3545',
        'descricao': 'Descarte na lixeira VERMELHA. Reciclável.'
    },
    'metal': {
        'nome': 'Metal',
        'cor_lixeira': 'Amarelo',
        'hex_cor': '#ffc107',
        'descricao': 'Descarte na lixeira AMARELA. Reciclável.'
    },
    'glass': {
        'nome': 'Vidro',
        'cor_lixeira': 'Verde',
        'hex_cor': '#28a745',
        'descricao': 'Descarte na lixeira VERDE. Reciclável.'
    },
    'trash': {
        'nome': 'Não Reciclável',
        'cor_lixeira': 'Cinza',
        'hex_cor': '#6c757d',
        'descricao': 'Material não reciclável. Descarte no lixo comum/orgânico.'
    }
}

def classify_image(image_path, model):
    """
    Função para carregar, pré-processar e classificar uma imagem.
    """
    if model is None:
        return ["error", 0]
        
    try:
        img = load_img(image_path, target_size=(299, 299))
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
    except Exception as e:
        print(f"❌ ERRO ao carregar ou pré-processar a imagem: {e}")
        return ["error", 0]

    try:
        predictions = model.predict(img_array)
        class_labels = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']
        predicted_class_index = np.argmax(predictions[0])
        predicted_class_label = class_labels[predicted_class_index]
        confidence = np.max(predictions[0])
        print(f"✅ Classe prevista: {predicted_class_label} (Confiança: {confidence*100:.2f}%)")
        return [predicted_class_label, confidence]
    except Exception as e:
        print(f"❌ ERRO ao fazer a previsão: {e}")
        return ["error", 0]


# --- Rotas da Aplicação ---

@app.route('/')
def index():
    """ Rota principal que renderiza o formulário de upload. """
    # Certifique-se de que o nome 'index.html' corresponde ao seu arquivo na pasta de templates
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """ Rota que recebe o arquivo do formulário e mostra o resultado. """
    if 'image' not in request.files:
        return redirect(request.url)

    file = request.files['image']

    if file.filename == '':
        return redirect(request.url)

    if file and model:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        print(f"✅ Arquivo '{filename}' salvo em '{filepath}'")
        
        # Chama a função de classificação
        prediction_result = classify_image(filepath, model)
        predicted_label = prediction_result[0]
        confidence = prediction_result[1]
        
        # ### NOVO: Busca as informações no dicionário ###
        # Usamos .get() para evitar erros caso a chave não exista, retornando um valor padrão.
        default_info = {'nome': 'Desconhecido', 'cor_lixeira': 'Cinza', 'hex_cor': '#6c757d', 'descricao': 'Não foi possível identificar o material.'}
        result_info = recycling_info_map.get(predicted_label, default_info)
        
        # Renderiza a página de resultado, passando todas as informações necessárias
        return render_template('upload/result.html', 
                               filename=filename, 
                               result_info=result_info, 
                               confidence=confidence)

    return redirect(url_for('index')) # Redireciona se algo der errado

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """ Rota para servir os arquivos da pasta de uploads para exibição no HTML. """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# --- Inicialização do Servidor com ngrok ---
if __name__ == '__main__':
    # Define a porta do Flask
    port = 5000
    
    # Abre um túnel HTTP para a porta 5000
    public_url = ngrok.connect(port)
    print("====================================================================")
    print(f"✅ Link público para a apresentação: {public_url}")
    print("====================================================================")
    print("Pressione CTRL+C para encerrar o servidor e o túnel do ngrok.")

    # Inicia o servidor Flask
    app.run(port=port)