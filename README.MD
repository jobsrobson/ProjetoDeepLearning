# Recicla.AI - Identificador de Recicláveis com IA ♻️

## 📖 Sobre o Projeto
O **Recicla.AI** é uma aplicação web inteligente que utiliza um modelo de Deep Learning para ajudar os usuários a descartar seus resíduos corretamente. Ao enviar uma foto de um objeto, a nossa Inteligência Artificial o classifica em uma das categorias da coleta seletiva (papel, plástico, metal, vidro ou orgânico/não reciclável) e indica a cor da lixeira correta para o descarte.

Este projeto foi desenvolvido como uma demonstração prática do uso de Redes Neurais Convolucionais (CNNs) para classificação de imagens em um problema do mundo real, com foco em sustentabilidade e educação ambiental.

## ✨ Como Funciona
O processo é simples e intuitivo, dividido em três etapas:

1. **Upload da Imagem**: O usuário tira uma foto ou seleciona uma imagem do objeto a ser descartado.
2. **Análise com IA**: A imagem é enviada para o nosso servidor, onde um modelo de Deep Learning (baseado na arquitetura InceptionV3) a analisa.
3. **Resultado Instantâneo**: A aplicação retorna o tipo de material identificado, a cor da lixeira correspondente e o nível de confiança da previsão.

## 🚀 Principais Recursos
- **Classificação Automática**: Identifica 6 categorias de resíduos (papel, papelão, plástico, metal, vidro e lixo comum).
- **Interface Web Amigável**: Design limpo e responsivo para uma experiência de usuário agradável em qualquer dispositivo.
- **Indicação Visual**: Mostra a cor da lixeira correta, facilitando a memorização e o descarte adequado.
- **Modelo de Alta Precisão**: Utiliza um modelo de Deep Learning treinado com um vasto conjunto de imagens para garantir alta acurácia.
- **API Flask**: Construído sobre um backend robusto em Python com Flask.

## 💻 Tecnologias Utilizadas
- **Backend**: Python, Flask
- **Deep Learning**: TensorFlow, Keras
- **Frontend**: HTML5, Tailwind CSS

## 👨‍💻 Assista a Apresentação
Você pode assistir a uma apresentação do projeto no Figma: [Assista aqui](https://www.figma.com/deck/FlZJyTo3Q3Drv52RpnbIvf/Recicla.AI?node-id=19-60&t=UCv6MSy0oCYXEVJl-1).

## ▶️ Como Executar o Projeto
Você pode executar esta aplicação de duas maneiras: localmente em sua máquina ou diretamente no Google Colab.

#### Executando Localmente
Pré-requisitos:
- Python 3.9 ou superior
- Git

```
# 1. Clone o repositório
git clone [https://github.com/jobsrobson/ProjetoDeepLearning.git](https://github.comjobsrobson/ProjetoDeepLearning.git)

# 2. Entre na pasta do projeto
cd ProjetoDeepLearning

# 3. Crie e ative um ambiente virtual (recomendado)
# No Windows:
python -m venv venv
venv\Scripts\activate
# No macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# 4. Instale as dependências
pip install -r requirements.txt

# 5. Execute a aplicação Flask
# (O arquivo principal está em flaskr/__init__.py)
flask --app flaskr run
``` 

Acesse http://127.0.0.1:5000 no seu navegador.


#### Executando via Google Colab
Para facilitar a demonstração sem a necessidade de configuração local, você pode usar o Google Colab para rodar a aplicação e gerar um link público com ngrok.

Passos:

1. Abra o Notebook: [Clique aqui](https://colab.research.google.com/drive/1cuQNo_WoTij9IowcGoTLzmjg_PFZQEOC?usp=sharing) para abrir o notebook no Google Colab.
2. Configure seu Token do Ngrok (Obrigatório):

    - No menu à esquerda do Colab, clique no ícone de chave (🔑) para abrir o painel de "Segredos".
    - Clique em "+ Adicionar novo segredo".
    - No campo name, digite NGROK_AUTH_TOKEN.
    - No campo value, cole o seu token de autenticação do ngrok. Você pode obter um gratuitamente em ngrok.com.
    - Importante: Ative a chavinha "Acesso do notebook".

    **Nota de Segurança**: O recurso "Segredos" do Colab é pessoal e vinculado à sua conta Google. Outras pessoas que abrirem o notebook não terão acesso ao seu token e precisarão seguir o passo 2 para configurar o próprio token. Esta é a prática recomendada para manter as chaves de acesso seguras.

3. Execute as Células: Execute todas as células do notebook em ordem. A última célula irá clonar este repositório, iniciar a aplicação e fornecer um link público (.ngrok-free.app) para você acessar o projeto.


## 📂 Estrutura do Projeto
```
ProjetoDeepLearning/
├── flaskr/
│   ├── __init__.py           # Lógica principal da aplicação Flask e rotas
│   ├── modelo_garbage_inception_v1.keras # Modelo de IA
│   ├── templates/            # Arquivos HTML
│   │   ├── index.html
│   │   └── upload/
│   │       └── result.html
│   └── file_uploaded/        # Pasta para onde as imagens são enviadas (criada em tempo de execução)
├── requirements.txt          # Dependências do projeto
└── README.md                 # Este arquivo
```

## 📝 Licença
Este projeto está sob a licença GPL-3.0. Veja o arquivo LICENSE para mais detalhes.

## 👨‍💻 Autores
- [Robson Ricardo](https://github.com/jobsrobson)
- [Felipe Toledo](https://github.com/snowstoledo)
- [Guilherme Duarte](https://github.com/guirocduarte)
