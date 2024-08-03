import os
import requests
from PIL import Image
from io import BytesIO

def download_image(url, save_path):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
        
        image = Image.open(BytesIO(response.content))
        
        # Convert image to PNG format
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        image.save(save_path, 'PNG')
        
        print(f'Downloaded and saved as PNG {os.path.basename(save_path)}')
    except Exception as e:
        print(f'Erro ao baixar {url}: {e}')

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
            response = requests.head(url, allow_redirects=True)
            response.raise_for_status()
            
            content_type = response.headers.get('Content-Type', '')
            if 'image' not in content_type:
                print(f'URL {url} não é uma imagem.')
                continue

            filename = os.path.basename(url.split('?')[0]) + '.png'
            file_path = os.path.join(download_folder, filename)
            
            download_image(url, file_path)
            
            processed_count += 1
        except Exception as e:
            print(f'Erro ao baixar {url}: {e}')
    
    if processed_count == 0:
        print(f"Nenhuma imagem foi baixada. Verifique o arquivo '{txt_file}'.")