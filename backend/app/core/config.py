import os
from typing import Final

from dotenv import load_dotenv


# Carrega o arquivo `.env` antes de ler as variáveis de ambiente.
# Assim as credenciais ficam centralizadas e não precisam serem
# repetidas pelo código da aplicação.
load_dotenv()


# Valor padrão (inseguro) utilizado apenas em desenvolvimento.
# Em produção, a aplicação NUNCA deve utilizar este valor.
DEFAULT_INSECURE_SECRET_KEY: Final = "dev-secret-key-insecure"

# Credenciais padrão que não devem aparecer em DATABASE_URL em produção.
DEFAULT_DB_CREDENTIALS: Final = (
    "user:password",
    "usuario:senha",
)


class Settings:
    """Configurações da aplicação carregadas a partir de variáveis de ambiente.

    As variáveis contam com *fallback seguro* para garantir que a
    aplicação sempre inicialize, mesmo quando o arquivo `.env` não
    está presente ou está incompleto. Em produção, nunca deixe de
    definir ``DATABASE_URL`` e ``SECRET_KEY`` no ``.env``.
    """

    # --- Ambiente -------------------------------------------------------
    # Determina o ambiente de execução. Em "production" as validações
    # de segurança (veja :meth:`validate`) são aplicadas rigorosamente.
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

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
        DEFAULT_INSECURE_SECRET_KEY,  # valor de desenvolvimento; NÃO usar em produção
    )

    def validate(self) -> None:
        """Valida credenciais sensíveis conforme o ambiente configurado.

        Em ambientes que não sejam produção, nenhuma restrição é imposta —
        isso permite o uso de valores padrão durante o desenvolvimento e
        testes locais. Em produção, tanto ``SECRET_KEY`` quanto
        ``DATABASE_URL`` são verificadas para garantir que nenhuma
        credencial padrão ou frágil esteja em uso.
        """
        if self.ENVIRONMENT.lower() != "production":
            return

        # --- SECRET_KEY -------------------------------------------------
        if not self.SECRET_KEY or self.SECRET_KEY == DEFAULT_INSECURE_SECRET_KEY:
            raise RuntimeError(
                "SECRET_KEY não pode ser vazia ou o valor padrão "
                f"'{DEFAULT_INSECURE_SECRET_KEY}' em produção. "
                "Defina uma chave secreta forte no .env."
            )

        # --- DATABASE_URL -----------------------------------------------
        if any(cred in self.DATABASE_URL for cred in DEFAULT_DB_CREDENTIALS):
            raise RuntimeError(
                "DATABASE_URL contém credenciais padrão em produção. "
                "Defina uma URL de banco com credenciais seguras no .env."
            )


# Instância única de configurações compartilhada por toda a aplicação.
settings: Settings = Settings()

# Em produção, garante que nenhuma credencial padrão ou frágil esteja ativa
# antes de a aplicação iniciar.
settings.validate()

# Variáveis de módulo mantidas por compatibilidade com consumidores
# (ex.: `main.py`, `tests/conftest.py`) que importam diretamente.
DATABASE_URL: Final[str] = settings.DATABASE_URL
SECRET_KEY: Final[str] = settings.SECRET_KEY
ENVIRONMENT: Final[str] = settings.ENVIRONMENT

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
