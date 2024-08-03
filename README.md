# Background Remover

## Descrição

O **Background Remover** é uma ferramenta projetada para remover o fundo de imagens. Este projeto é voltado para uso pessoal e foi criado para facilitar a edição de imagens, especialmente quando se deseja isolar o assunto principal de uma foto. O projeto oferece duas principais funcionalidades: processar imagens de uma pasta local ou baixar imagens de URLs listadas em um arquivo `.txt` e então processá-las.

## Funcionalidades

- **Remoção de Fundo**: Remove o fundo das imagens usando uma função de processamento de imagem.
- **Processamento de Pasta Local**: Permite processar imagens diretamente de uma pasta local.
- **Download e Processamento de Imagens**: Faz o download de imagens a partir de URLs listadas em um arquivo `.txt` e processa essas imagens.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação principal.
- **Pillow**: Biblioteca para manipulação de imagens.
- **rembg**: Biblioteca para remoção de fundo de imagens.
- **requests**: Biblioteca para fazer download de imagens da web.

## Instalação

Para usar o **Background Remover**, você precisa ter o Python instalado no seu sistema. Além disso, você deve instalar as dependências necessárias. Para fazer isso, clone o repositório e instale as dependências com `pip`:

```bash
git clone https://github.com/rodrigueskaua/Background-Remover.git
cd Background-Remover
pip install -r requirements.txt
