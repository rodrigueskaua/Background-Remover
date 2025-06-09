import os
from werkzeug.utils import secure_filename
from .downloader import download_image
from .background_remover import process_single_image

def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def save_uploaded_files(files, destination_folder, allowed_extensions):
    saved_paths = []
    for file in files:
        if file and file.filename and allowed_file(file.filename, allowed_extensions):
            filename = secure_filename(file.filename)
            file_path = os.path.join(destination_folder, filename)
            file.save(file_path)
            saved_paths.append(file_path)
    return saved_paths

def save_url_images(urls, destination_folder, allowed_extensions):
    saved_paths = []
    for i, url in enumerate(filter(None, urls)):
        url = url.strip()
        if not url:
            continue
            
        base_name = os.path.basename(url).split('?')[0]
        if not allowed_file(base_name, allowed_extensions):
            base_name = f"url_image_{i}.png"
            
        filename = secure_filename(base_name)
        file_path = os.path.join(destination_folder, filename)
        if download_image(url, file_path):
            saved_paths.append(file_path)
            
    return saved_paths

def process_images_in_paths(input_paths, output_folder):
    processed_paths = []
    for input_path in input_paths:
        filename = os.path.basename(input_path)
        output_filename = os.path.splitext(filename)[0] + '.png'
        output_path = os.path.join(output_folder, output_filename)
        
        try:
             # 2. Chame a nova função com o nome correto
             process_single_image(input_path, output_path)
             processed_paths.append(output_path)
        except Exception as e:
            print(f"Erro ao processar {filename}: {e}")

    return processed_paths