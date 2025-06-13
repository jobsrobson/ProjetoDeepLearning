import os
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

# --- Configuração Inicial ---
app = Flask(__name__, template_folder="template")

# Configura o caminho para a pasta de uploads
UPLOAD_FOLDER = 'file_uploaded'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Garante que a pasta de uploads exista
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Carrega o modelo de IA pré-treinado (MobileNetV2) uma única vez ao iniciar o servidor
# Isso evita recarregar o modelo a cada requisição, o que seria muito lento.


def classify_image(image_path):
    """
    Função para carregar uma imagem, pré-processá-la e classificá-la usando o modelo MobileNetV2.
    """
    return [[1, "Orgâncio", 0.95]]  # Simulação de classificação

# --- Rotas da Aplicação ---

@app.route('/')
def index():
    """ Rota principal que renderiza o formulário de upload. """
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """ Rota que recebe o arquivo do formulário. """
    if 'image' not in request.files:
        return redirect(request.url) # Redireciona de volta se nenhum arquivo for enviado

    file = request.files['image']

    if file.filename == '':
        return redirect(request.url) # Redireciona se o nome do arquivo for vazio

    if file:
        # Garante um nome de arquivo seguro para evitar problemas de segurança
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Chama a função de classificação
        predictions = classify_image(filepath)
        
        # Renderiza a página de resultado, passando o nome do arquivo e as predições
        return render_template('upload/result.html', filename=filename, predictions=predictions)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """ Rota para servir os arquivos da pasta 'uploads' para que possam ser exibidos no HTML. """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)