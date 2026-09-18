import os
from typing import Final

from dotenv import load_dotenv


# Carrega o arquivo `.env` antes de ler as variáveis de ambiente.
# Assim as credenciais ficam centralizadas e não precisam serem
# repetidas pelo código da aplicação.
load_dotenv()


class Settings:
    """Configurações da aplicação carregadas a partir de variáveis de ambiente.

    As variáveis contam com *fallback seguro* para garantir que a
    aplicação sempre inicialize, mesmo quando o arquivo `.env` não
    está presente ou está incompleto. Em produção, nunca deixe de
    definir ``DATABASE_URL`` e ``SECRET_KEY`` no ``.env``.
    """

    # --- Banco de dados -------------------------------------------------
    # Formato esperado:
    #   postgresql+psycopg2://usuario:senha@host:5432/nome_do_banco
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://user:password@localhost:5432/controle_produtos",
    )

    # --- Segurança ------------------------------------------------------
    # Chave secreta utilizada para assinar tokens JWT e outras credenciais
    # sensíveis. Em ambientes de produção, sempre defina `SECRET_KEY` no
    # arquivo `.env` para evitar que a chave padrão seja usada.
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "dev-secret-key-insecure",  # valor de desenvolvimento; NÃO usar em produção
    )


# Instância única de configurações compartilhada por toda a aplicação.
settings: Settings = Settings()

# Variáveis de módulo mantidas por compatibilidade com consumidores
# (ex.: `main.py`, `tests/conftest.py`) que importam diretamente.
DATABASE_URL: Final[str] = settings.DATABASE_URL
SECRET_KEY: Final[str] = settings.SECRET_KEY

# ---------------------------------------------------------------------------
# Como configurar as credenciais do banco
# ---------------------------------------------------------------------------
# - Crie um arquivo `.env` na raiz do projeto (mesmo nível de `send_product.py`).
# - Defina as variáveis `DATABASE_URL` e `SECRET_KEY` dentro dele.
# - Exemplo de formato:
#   DATABASE_URL=postgresql+psycopg2://usuario:senha@host:5432/nome_do_banco
#   SECRET_KEY=sua-chave-secreta-aqui
#
# Bibliotecas utilizadas:
# - `os`             – lê variáveis de ambiente.
# - `python-dotenv`  – carrega automaticamente as variáveis do `.env` via `load_dotenv`.
