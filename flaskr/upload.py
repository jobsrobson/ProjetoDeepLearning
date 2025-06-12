import os

from flask import (
    Blueprint, flash, redirect, request, url_for
)

from werkzeug.utils import secure_filename

bp = Blueprint('upload', __name__, url_prefix='/')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg'}

@bp.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('Parte do arquivo não encontrada')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('Nenhum arquivo selecionado')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('file_uploaded', filename))
            return redirect(url_for('download_file', name=filename))
    
