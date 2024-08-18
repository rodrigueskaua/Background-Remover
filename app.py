from flask import Flask, render_template, request, jsonify, redirect, url_for
from src.background_remover import remove_background
from config import Config
from src.utils import create_folders, convert_images, process_files

app = Flask(__name__)
app.config.from_object(Config)

create_folders([app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER']])

@app.route('/')
def index():
    return redirect(url_for('background_remover'))

@app.route('/background-remover', methods=['GET', 'POST'])
def background_remover():
    if request.method == 'POST':
        if 'files[]' in request.files:
            files = request.files.getlist('files[]')
            process_files(files, app.config['UPLOAD_FOLDER'], app.config['ALLOWED_EXTENSIONS'])
            return convert_images(app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER'])

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
