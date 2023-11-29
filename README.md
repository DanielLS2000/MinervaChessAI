# MinervaChessAI
Este guia fornece instruções passo a passo sobre como configurar um ambiente virtual Python, instalar pacotes a partir de um arquivo requirements.txt e executar o arquivo ChessInterface.py.

Configurando o Ambiente Virtual

1. Instale o Virtualenv (se ainda não estiver instalado):
   pip install virtualenv

2. Crie um Ambiente Virtual:
   virtualenv nome_do_seu_ambiente -p python3

Substitua nome_do_seu_ambiente pelo nome desejado para seu ambiente virtual.

3. Ative o Ambiente Virtual:

No Windows:
   nome_do_seu_ambiente\Scripts\activate

No macOS e Linux:
   source nome_do_seu_ambiente/bin/activate

Instalando Pacotes do requirements.txt

1. Navegue até o Diretório do Projeto:
   cd caminho/do/seu/projeto

2. Instale os Pacotes do requirements.txt:
   pip install -r requirements.txt

Certifique-se de que o arquivo requirements.txt esteja presente no diretório do projeto.

Executando o ChessInterface

1. Execute o Arquivo ChessInterface.py:
   python ChessInterface.py

Certifique-se de estar no ambiente virtual criado antes de executar este comando.
