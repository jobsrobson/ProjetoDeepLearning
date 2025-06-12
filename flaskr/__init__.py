import os

from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

def create_app(test_config=None):
    UPLOAD_FOLDER = '/file_uploaded'
    ALLOWED_EXTENSIONS = {'png', 'jpg'}

    def allowed_file(filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True, template_folder="template")
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    #from . import upload
    #app.register_blueprint(upload.bp)

    @app.route('/')
    def index():
        return  render_template("index.html")
    
    @app.route('/', methods=['GET', 'POST'])
    def upload_file():
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                print(f"File saved to {os.path.join(app.config['UPLOAD_FOLDER'], filename)}")
                return redirect(request.url)
        return '''
        <form action="/" method="post" enctype="multipart/form-data" class="w-full">
        <div class="flex flex-col items-center">
          <div id="dropzone" class="dropzone bg-white rounded-lg p-8 w-full max-w-md mb-6 cursor-pointer">
            <div class="flex flex-col items-center">
              <i class="fas fa-cloud-upload-alt text-4xl text-indigo-500 mb-4"></i>
              <p class="text-gray-700">Arraste e solte uma imagem aqui ou</p>

              <input id="arquivoBtn" type="file" value="Selecione um arquivo" class="mt-2 px-6 py-2 rounded-md">
              </input>


              <input type="file" id="fileInput" accept="image/*" class="hidden">
            </div>
          </div>
          <p class="text-sm text-gray-500">Formatos suportados: JPG, PNG (Máx. 5MB)</p>
        </div>

        <input id="enviarBtn" type="submit" value="Enviar Imagem"
          class="mt-2 bg-indigo-600 text-white px-6 py-2 rounded-md hover:bg-indigo-700 transition">
        </input>
        </form>
        '''

    
    return app
