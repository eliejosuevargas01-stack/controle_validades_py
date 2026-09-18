import os

from dotenv import load_dotenv


# Carrega o arquivo `.env` antes de ler as variáveis de ambiente.
# Assim `DATABASE_URL` fica disponível sem repetir credenciais no código.
load_dotenv()


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://user:password@localhost:5432/controle_produtos",
)

#
# Chave secreta utilizada para assinar tokens JWT e outras credenciais sensíveis.
# Em ambientes de produção, sempre defina `SECRET_KEY` no arquivo `.env` para
# evitar que a chave padrão seja usada.
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "dev-secret-key-insecure",  # valor de desenvolvimento; NÃO usar em produção
)

# Onde colocar as credenciais do banco:
# - crie um arquivo `.env` na raiz do projeto, no mesmo nível de `send_product.py`
# - coloque nele a variável `DATABASE_URL`
# - exemplo de formato:
#   DATABASE_URL=postgresql+psycopg2://usuario:senha@host:5432/nome_do_banco
#
# Se você usar `.env`, a aplicação deve carregar essas variáveis antes de abrir a conexão.
# Isso evita deixar usuário, senha e host espalhados pelo código.
#
# Onde entram as bibliotecas:
# - `os` para ler variáveis de ambiente
# - `python-dotenv` ou equivalente, se você decidir carregar o arquivo `.env` automaticamente
# - essa parte fica antes de qualquer conexão com o banco ser criada
