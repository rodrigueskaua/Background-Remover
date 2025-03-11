from flask import Flask, render_template, request, jsonify, redirect, url_for
from src.background_remover import remove_background
from config import Config
from src.utils import create_folders, convert_images, process_files, process_urls, open_processed_folder

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
            result = convert_images(app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER'])
            open_processed_folder()
            return result
        
        elif 'urls' in request.form:
            urls = request.form.get('urls').split('\n')
            process_urls(urls, app.config['UPLOAD_FOLDER'])
            result = convert_images(app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER'])
            open_processed_folder()
            return result
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
