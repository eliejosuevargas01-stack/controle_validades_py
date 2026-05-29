from pathlib import Path
import os

from sqlalchemy import create_engine, inspect, text

from app.db.init_db import init_db


def load_database_url():
    # Primeiro tenta usar a variável de ambiente já carregada.
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    # Se não estiver no ambiente, lê direto do arquivo .env na raiz do projeto.
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("DATABASE_URL="):
                return line.split("=", 1)[1].strip()

    raise RuntimeError("DATABASE_URL nao encontrada no ambiente nem no arquivo .env")


def test_database_connection():
    # Teste simples para confirmar que o PostgreSQL responde à aplicação.
    engine = create_engine(load_database_url())
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        assert result.scalar() == 1


def test_products_catalog_table_exists():
    # Garante que o banco consegue criar a tabela fixa de catalogo de produtos.
    init_db()
    engine = create_engine(load_database_url())
    inspector = inspect(engine)
    assert inspector.has_table("products_catalog")


def test_validades_has_usuario_id():
    # Garante que a tabela operacional de validades tem ligacao com o usuario logado.
    init_db()
    engine = create_engine(load_database_url())
    inspector = inspect(engine)
    columns = {column["name"] for column in inspector.get_columns("validades")}
    assert "usuario_id" in columns

    foreign_keys = inspector.get_foreign_keys("validades")
    assert any(
        fk.get("constrained_columns") == ["usuario_id"]
        and fk.get("referred_table") == "validade_login"
        for fk in foreign_keys
    )
