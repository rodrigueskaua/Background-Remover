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
        
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        image.save(save_path, 'PNG')
        
        print(f'Downloaded and saved as PNG {os.path.basename(save_path)}')
    except Exception as e:
        print(f'Erro ao baixar {url}: {e}')
