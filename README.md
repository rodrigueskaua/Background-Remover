# Background Remover

## Descrição

O **Background Remover** é uma ferramenta projetada para remover o fundo de imagens. Este projeto é voltado para uso pessoal e facilita a edição de imagens, especialmente quando se deseja isolar o assunto principal de uma foto. O projeto oferece duas formas principais de interação:

1. **Interface Web**: Uma interface web criada com Flask, HTML, e CSS, que permite o envio de imagens para remoção de fundo e o download das imagens processadas.
2. **Terminal**: Um script de terminal que permite executar o processo de remoção de fundo diretamente do terminal.

## Funcionalidades

### Interface Web (`app.py`)

- **Upload de Imagens**: Permite o upload de imagens diretamente do navegador.
- **Adição de URLs**: Permite adicionar URLs de imagens para download e processamento.
- **Conversão de Imagens**: Após o upload ou download das imagens, você pode clicar em "Converter Imagens" para remover o fundo.
- **Mensagens Interativas**: Utiliza SweetAlert2 para exibir mensagens de progresso e resultados de forma interativa.

### Terminal (`terminal.py`)

- **Processamento Local**: Permite processar imagens a partir de uma pasta local diretamente do terminal.
- **Execução Direta**: Você pode executar o script para remover o fundo de todas as imagens em uma pasta sem necessidade de uma interface gráfica.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação principal.
- **Flask**: Framework para criar a interface web.
- **Pillow**: Biblioteca para manipulação de imagens.
- **rembg**: Biblioteca para remoção de fundo de imagens.
- **requests**: Biblioteca para fazer download de imagens da web.
- **SweetAlert2**: Biblioteca para exibir mensagens interativas na interface web.

## Instalação

Para usar o **Background Remover**, siga os passos abaixo:

1. Clone o repositório e navegue até o diretório do projeto:

    ```bash
    git clone https://github.com/rodrigueskaua/Background-Remover.git
    cd Background-Remover
    ```

2. Instale as dependências necessárias:

    ```bash
    pip install -r requirements.txt
    ```

## Uso

### Interface Web

1. Inicie o servidor Flask:

    ```bash
    python app.py
    ```

2. Abra o navegador e vá para `http://127.0.0.1:5000/` para acessar a interface web.
3. Faça o upload das imagens ou adicione URLs para download e conversão. Clique em "Converter Imagens" para processar as imagens.

### Terminal

1. Execute o script `terminal.py` para processar em uma pasta local ou selecionar o arquivo com links:

    ```bash
    python terminal.py
    ```

2. As imagens processadas serão salvas na pasta de saída especificada.


