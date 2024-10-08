from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
import os
import webbrowser
import subprocess
from werkzeug.utils import secure_filename
from src.background_remover import remove_background
from src.downloader import download_images_from_txt
import sys

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output_images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

for folder in [app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER']]:
    if not os.path.exists(folder):
        os.makedirs(folder)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return redirect(url_for('background_remover'))

@app.route('/background-remover', methods=['GET', 'POST'])
def background_remover():
    if request.method == 'POST':
        if 'files[]' in request.files:
            files = request.files.getlist('files[]')
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify({'success': True, 'message': 'Imagens enviadas com sucesso!'})

        if 'urls' in request.form:
            urls = request.form['urls'].splitlines()
            txt_file = 'temp_urls.txt'
            with open(txt_file, 'w') as f:
                for url in urls:
                    f.write(f"{url.strip()}\n")

            download_folder = app.config['UPLOAD_FOLDER']
            download_images_from_txt(txt_file, download_folder)
            os.remove(txt_file)
            return jsonify({'success': True, 'message': 'Imagens baixadas com sucesso!'})

    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_images():
    try:
        remove_background(app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER'])
        # Delete the files in the upload folder after conversion
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

        # Open the output folder
        open_folder(app.config['OUTPUT_FOLDER'])

        return jsonify({'success': True, 'message': 'Imagens convertidas com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

def open_folder(path):
    """Open the folder in the file explorer."""
    if os.name == 'nt':  # Windows
        os.startfile(path)
    elif os.name == 'posix':  # macOS or Linux
        subprocess.call(['open' if sys.platform == 'darwin' else 'xdg-open', path])

if __name__ == '__main__':
    # Open the default web browser
    webbrowser.open('http://localhost:5000/')
    app.run(debug=True)
