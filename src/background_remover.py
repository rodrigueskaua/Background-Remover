from PIL import Image
from rembg import remove
import numpy as np
import os

def process_single_image(input_path: str, output_path: str):
    """
    Processa uma única imagem para remover o fundo, cortar o espaço extra
    e salvar no caminho de saída.

    Args:
        input_path (str): O caminho completo para a imagem de entrada.
        output_path (str): O caminho completo onde a imagem processada será salva.
    """
    if not os.path.exists(input_path):
        print(f"Erro: Arquivo de entrada não encontrado em {input_path}")
        return

    try:
        with Image.open(input_path) as img:
            # Remover o fundo
            img_no_bg = remove(img)
            
            # Cortar o espaço transparente extra (autocrop)
            img_array = np.array(img_no_bg)
            
            # Verifica se a imagem tem um canal alfa (transparência)
            if img_array.shape[2] < 4:
                # Se não tiver, salva a imagem como está (pode ser um erro do rembg)
                img_no_bg.save(output_path, 'PNG')
                print(f"A imagem {os.path.basename(input_path)} não retornou um canal alfa. Salva como está.")
                return

            non_empty_columns = np.where(img_array[:, :, 3] > 0)[1]
            non_empty_rows = np.where(img_array[:, :, 3] > 0)[0]
            
            if non_empty_columns.size > 0 and non_empty_rows.size > 0:
                left = non_empty_columns.min()
                right = non_empty_columns.max()
                top = non_empty_rows.min()
                bottom = non_empty_rows.max()
                
                # Adiciona uma pequena margem para não cortar muito perto
                padding = 5
                left = max(0, left - padding)
                top = max(0, top - padding)
                right = min(img_no_bg.width, right + padding)
                bottom = min(img_no_bg.height, bottom + padding)

                img_cropped = img_no_bg.crop((left, top, right, bottom))
            else:
                # Se não houver conteúdo (imagem toda transparente), não faz nada ou salva a imagem vazia
                img_cropped = img_no_bg
            
            # Salvar a imagem cortada
            img_cropped.save(output_path, 'PNG')
            print(f"Processado com sucesso: {os.path.basename(input_path)}")

    except Exception as e:
        print(f"Falha ao processar a imagem {os.path.basename(input_path)}: {e}")