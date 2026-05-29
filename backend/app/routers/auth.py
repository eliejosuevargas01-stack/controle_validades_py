from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Imports que vamos ligar depois:
# from app.db.session import get_db
# from app.schemas.auth import LoginRequest, LoginResponse
# from app.services.auth_service import authenticate_user
from app.db.session import get_db
from app.schemas.auth import LoginRequest, LoginResponse, SignUpRequest, SignUpResponse
from app.services.auth_service import authenticate_user, create_user
# Router do modulo auth.
# Este arquivo apenas recebe requests, chama os services e devolve respostas.

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(playload: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, playload.email, playload.senha)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos",
        )
    return user


# Rota de cadastro.
# O payload entra validado pelo schema e o service decide se pode salvar.
@router.post("/signup", response_model=SignUpResponse)
def signup(playload: SignUpRequest, db: Session = Depends(get_db)):
    try:
        user = create_user(
            db=db,
            email=playload.email,
            senha=playload.senha,
            loja=playload.loja,
            business=playload.business,
            whatsapp=playload.whatsapp
        )
        return user
    except ValueError as e:
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
    )  


# Tarefas futuras para o modulo auth:
# - padronizar nomes de variaveis para "payload" em vez de "playload"
# - trocar ValueError por excecoes HTTP mais especificas quando fizer sentido
# - adicionar testes de dados invalidos no signup
# - adicionar hash de senha e remover comparacao em texto puro
# - separar login e signup em arquivos diferentes se surgir mais logica
