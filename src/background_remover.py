import os
from PIL import Image
from rembg import remove
import numpy as np

def remove_background(input_folder, output_folder):
    if not os.path.exists(input_folder):
        print(f"Erro: A pasta de entrada '{input_folder}' não existe.")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    processed_count = 0
    messages = []
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            input_path = os.path.join(input_folder, filename)
            output_filename = os.path.splitext(filename)[0] + '.png'
            output_path = os.path.join(output_folder, output_filename)
            
            try:
                with Image.open(input_path) as img:
                    if img.mode != 'RGBA':
                        img = img.convert('RGBA')
                    
                    # Remover o fundo
                    img_no_bg = remove(img)
                    
                    # Converter para formato de array para processamento
                    img_array = np.array(img_no_bg)
                    
                    # Identificar a região com conteúdo
                    non_empty_columns = np.where(img_array[:, :, 3] > 0)[1]
                    non_empty_rows = np.where(img_array[:, :, 3] > 0)[0]
                    
                    if non_empty_columns.size > 0 and non_empty_rows.size > 0:
                        # Definir a área de corte
                        left = non_empty_columns.min()
                        right = non_empty_columns.max()
                        top = non_empty_rows.min()
                        bottom = non_empty_rows.max()
                        
                        # Realizar o crop
                        img_cropped = img_no_bg.crop((left, top, right, bottom))
                    else:
                        # Se não houver conteúdo, mantenha a imagem original
                        img_cropped = img_no_bg
                    
                    # Salvar a imagem cortada
                    img_cropped.save(output_path, format='PNG')
                
                print(f'Processed {filename}')
                messages.append(f'Processado {filename}')
                processed_count += 1
            except Exception as e:
                print(f'Erro ao processar {filename}: {e}')
                messages.append(f'Erro ao processar {filename}: {e}')
    
    if processed_count == 0:
        print(f"Nenhuma imagem foi processada. Verifique se há arquivos de imagem em '{input_folder}'.")
    
    return '\n'.join(messages)
