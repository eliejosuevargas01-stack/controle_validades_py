from sqlalchemy import Boolean, BigInteger, Column, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from app.db.base import Base


# Tabela operacional de validades.
# Ela guarda os registros efetivos que o usuario lança no dia a dia.
# O campo usuario_id liga cada linha ao usuario logado da tabela validade_login.
class ValidadeDB(Base):
    __tablename__ = "validades"

    id = Column(BigInteger, primary_key=True, index=True)
    adicionado_em = Column(DateTime, server_default=func.now(), nullable=True)
    nome = Column(String(255), nullable=False, index=True)
    validade = Column(Date, nullable=True, index=True)
    quantidade = Column(Integer, nullable=True, server_default="0")
    ean = Column(String(50), nullable=True, index=True)
    troca = Column(Boolean, nullable=True, server_default="false")
    rotatividade_alta = Column(Boolean, nullable=True, server_default="false")
    lancado = Column(Boolean, nullable=True, server_default="false")
    data_lancado = Column(DateTime, nullable=True)
    usuario = Column(String(50), nullable=True)
    categoria = Column(String(100), nullable=True, index=True)
    vendido = Column(Boolean, nullable=True)
    retirado = Column(Boolean, nullable=True)
    whatsapp = Column(String(20), nullable=True)
    usuario_id = Column(Integer, ForeignKey("validade_login.id"), nullable=True, index=True)
    deletado = Column(Boolean, nullable=False, server_default="false", index=True)
# Alias temporario para nao quebrar imports antigos durante a transicao.
ProductDB = ValidadeDB
