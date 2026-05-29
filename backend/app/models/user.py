from sqlalchemy import Boolean, Column, DateTime, Integer, Text, text
from sqlalchemy.sql import func

from app.db.base import Base


# Tabela de usuarios usada pelo modulo de auth.
# Ela representa a tabela real validade_login que ja existe no banco.
class UserDB(Base):
    __tablename__ = "validade_login"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(Text, nullable=False, unique=True, index=True)
    senha = Column(Text, nullable=False)
    loja = Column(Text, nullable=False)
    criado_em = Column(DateTime, server_default=func.now(), nullable=True)
    expira_em = Column(DateTime, server_default=text("(now() + '1 year'::interval)"), nullable=True)
    business = Column(Boolean, nullable=True)
    whatsapp = Column(Text, nullable=True)


# Alias para manter compatibilidade se algum arquivo antigo ainda usar o nome genérico.
User = UserDB
