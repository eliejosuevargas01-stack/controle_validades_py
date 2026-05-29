from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.security import create_access_token

def authenticate_user(db: Session, email: str, senha: str):
    # Busca o usuario pelo login e valida a senha.
    # Esta funcao apenas consulta e devolve os dados necessarios para o login.
    query = text (
        """
        SELECT id, login, loja, criado_em, expira_em, business, whatsapp, senha
        FROM validade_login
        WHERE login = :email
        LIMIT 1"""
    )

    user = db.execute(query, {"email": email}).mappings().first()
   

    # Usuario nao encontrado.
    if user is None:
        return None

    # Comparacao simples enquanto a senha ainda esta em texto puro.
    if user["senha"] != senha:
        return None

    # Devolve os dados esperados pelo schema de resposta.
    token = create_access_token(
        data={ "sub": str(user["id"])
        }
    )
    return {
        "access_token": token,
        "token_type": "bearer"
    }
    

def create_user(db, email, senha, loja, business, whatsapp):
    # Cria um novo usuario depois de verificar duplicidade.
    # O banco gera criado_em e expira_em automaticamente.
    query = text(
        """
        SELECT login
        FROM validade_login
        WHERE login = :email
        LIMIT 1
        """
    )

    existing_user = db.execute(query, {"email": email}).mappings().first()
    if existing_user:
        raise ValueError("Email already registered")

    # Insere o usuario e pede ao banco para devolver os campos gerados.
    query = text(
        """
        INSERT INTO validade_login (login, senha, loja, business, whatsapp)
        VALUES (:email, :senha, :loja, :business, :whatsapp)
        RETURNING id, login, loja, business, whatsapp, criado_em, expira_em
        """
    )
    result = db.execute(query, {
    "email": email,
    "senha": senha,
    "loja": loja,
    "business": business,
    "whatsapp": whatsapp
}).mappings().first()
    

    db.commit()
    
    return {
    "id": result["id"],
    "email": result["login"],
    "loja": result["loja"],
    "criado_em": result["criado_em"],
    "expira_em": result["expira_em"],
    "business": result["business"],
    "whatsapp": result["whatsapp"],
}


# Tarefas futuras para este modulo:
# - trocar senha em texto puro por hash seguro
# - trocar ValueError por excecoes mais especificas do dominio
# - separar login e signup em servicos distintos quando o projeto crescer
# - centralizar mensagens de erro para evitar texto duplicado na app
# - adicionar transacoes e rollback explicito nos fluxos sensiveis
