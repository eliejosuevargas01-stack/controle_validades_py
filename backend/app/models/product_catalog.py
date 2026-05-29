from sqlalchemy import Boolean, Column, Integer, String

from app.db.base import Base


# Tabela de catalogo fixo de produtos.
# Ela guarda apenas os dados mestre que podem ser reaproveitados
# quando o frontend pesquisar por nome ou ean.
class ProductCatalogDB(Base):
    __tablename__ = "products_catalog"

    id = Column(Integer, primary_key=True, index=True)
    ean = Column(String(32), unique=True, index=True, nullable=False)
    nome = Column(String(255), index=True, nullable=False)
    troca = Column(Boolean, nullable=False, default=False)
    rotatividade = Column(Boolean, nullable=False, default=False)
    categoria = Column(String(120), index=True, nullable=True)
