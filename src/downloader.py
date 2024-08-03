import os
import requests

def download_images_from_txt(txt_file, download_folder):
    if not os.path.exists(txt_file):
        print(f"Erro: O arquivo de URLs '{txt_file}' não existe.")
        return
    
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    processed_count = 0
    with open(txt_file, 'r') as file:
        urls = file.readlines()
    
    for url in urls:
        url = url.strip()
        if not url:
            continue
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            filename = os.path.basename(url)
            file_path = os.path.join(download_folder, filename)
            
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            print(f'Downloaded {filename}')
            processed_count += 1
        except Exception as e:
            print(f'Erro ao baixar {url}: {e}')
    
    if processed_count == 0:
        print(f"Nenhuma imagem foi baixada. Verifique o arquivo '{txt_file}'.")
