import os
from src.background_remover import remove_background
from src.downloader import download_images_from_txt

def ensure_directories_exist(*dirs):
    """Verifica se as pastas existem e as cria se não existirem."""
    for dir in dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)
            print(f"Pasta '{dir}' criada.")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    input_folder = os.path.join(script_dir, 'input_images')
    download_folder = os.path.join(script_dir, 'downloaded_images')
    output_folder = os.path.join(script_dir, 'output_images')
    
    ensure_directories_exist(input_folder, download_folder, output_folder)
    
    print("Escolha uma opção:")
    print("1. Processar imagens da pasta 'input_images'")
    print("2. Baixar imagens de URLs listadas em um arquivo .txt e processar")
    
    choice = input("Digite 1 ou 2: ").strip()
    
    if choice == '1':
      print(f"Processando imagens da pasta '{input_folder}' para a pasta '{output_folder}'...")
      remove_background(input_folder, output_folder)
    
    elif choice == '2':
      txt_file = input("Digite o caminho para o arquivo .txt com as URLs: ").strip()
      
      print(f"Baixando imagens do arquivo '{txt_file}' para a pasta '{download_folder}'...")
      download_images_from_txt(txt_file, download_folder)
      
      print(f"Processando imagens baixadas da pasta '{download_folder}' para a pasta '{output_folder}'...")
      remove_background(download_folder, output_folder)
    
    else:
      print("Opção inválida. Encerrando.")