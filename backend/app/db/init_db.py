from app.db.base import Base
from app.db.session import engine


def ensure_validades_usuario_id_column():
    # A tabela validades ja existe no banco, entao criamos apenas o que estiver faltando.
    from sqlalchemy import inspect, text

    inspector = inspect(engine)
    if "validades" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("validades")}

    if "usuario_id" not in columns:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE validades ADD COLUMN usuario_id INTEGER"))

    # A foreign key deixa pronto o relacionamento entre a validade e o usuario dono.
    inspector = inspect(engine)
    foreign_keys = inspector.get_foreign_keys("validades")
    fk_exists = any(
        fk.get("constrained_columns") == ["usuario_id"]
        and fk.get("referred_table") == "validade_login"
        and fk.get("referred_columns") == ["id"]
        for fk in foreign_keys
    )

    if not fk_exists:
        with engine.begin() as connection:
            connection.execute(
                text(
                    "ALTER TABLE validades "
                    "ADD CONSTRAINT fk_validades_usuario_id "
                    "FOREIGN KEY (usuario_id) REFERENCES validade_login (id)"
                )
            )


def init_db():
    import app.models.user  # noqa: F401
    import app.models.product  # noqa: F401
    import app.models.product_catalog  # noqa: F401

    Base.metadata.create_all(bind=engine)
    ensure_validades_usuario_id_column()
