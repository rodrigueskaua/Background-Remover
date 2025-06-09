import os
import uuid
import shutil
import zipfile
from io import BytesIO
from flask import Blueprint, render_template, request, current_app, send_file, jsonify
from . import utils

main_blueprint = Blueprint('main', __name__, static_folder='static', template_folder='templates')

@main_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    session_id = str(uuid.uuid4())
    
    temp_dir = current_app.config['TEMP_FOLDER']
    session_folder = os.path.join(temp_dir, session_id)
    input_folder = os.path.join(session_folder, 'input')
    output_folder = os.path.join(session_folder, 'output')
    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    try:
        files = request.files.getlist('files[]')
        urls = request.form.get('urls', '').strip().splitlines()
        allowed_extensions = current_app.config['ALLOWED_EXTENSIONS']

        if not files and not any(urls):
            return jsonify({'success': False, 'message': 'Nenhuma imagem ou URL foi enviada.'}), 400

        input_paths_from_files = utils.save_uploaded_files(files, input_folder, allowed_extensions)
        input_paths_from_urls = utils.save_url_images(urls, input_folder, allowed_extensions)
        all_input_paths = input_paths_from_files + input_paths_from_urls
        
        processed_paths = utils.process_images_in_paths(all_input_paths, output_folder)

        if len(processed_paths) == 1:
            return send_file(processed_paths[0], as_attachment=True)
        elif len(processed_paths) > 1:
            memory_file = BytesIO()
            with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
                for file_path in processed_paths:
                    zf.write(file_path, arcname=os.path.basename(file_path))
            memory_file.seek(0)
            return send_file(memory_file, download_name='imagens_processadas.zip', as_attachment=True)
        else:
            return jsonify({'success': False, 'message': 'Nenhuma imagem pôde ser processada.'}), 500

    finally:
        if os.path.exists(session_folder):
            shutil.rmtree(session_folder)