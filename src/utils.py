from flask import jsonify
import os
from werkzeug.utils import secure_filename
from src.background_remover import remove_background
from src.downloader import download_image

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def create_folders(folders):
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

def clean_upload_folder(upload_folder):
    for filename in os.listdir(upload_folder):
        file_path = os.path.join(upload_folder, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

def process_files(files, upload_folder, allowed_extensions):
    for file in files:
        if file and allowed_file(file.filename, allowed_extensions):
            filename = secure_filename(file.filename)
            file.save(os.path.join(upload_folder, filename))

def process_urls(urls, upload_folder):
    for url in urls:
        url = url.strip()
        if url:
            filename = os.path.join(upload_folder, os.path.basename(url) + '.png')
            download_image(url, filename)
            
def convert_images(upload_folder, output_folder):
    try:
        remove_background(upload_folder, output_folder)

        clean_upload_folder(upload_folder)

        return jsonify({'success': True, 'message': 'Imagens convertidas com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})