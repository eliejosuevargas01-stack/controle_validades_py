from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator

# Schemas do modulo de autenticacao.
# Este arquivo define a forma dos dados que entram e saem da API.

# Login:
# - entrada: email e senha
# - saida: dados do usuario autenticado
class LoginRequest(BaseModel):
    email: EmailStr = Field(..., max_length=255)
    senha: str

    @field_validator("email")
    @classmethod
    def normalizar_email(cls, v):
        return v.strip().lower()

    @field_validator("senha")
    @classmethod
    def validar_senha(cls, v):
        if len(v) < 6:
            raise ValueError("A senha deve ter pelo menos 6 caracteres.")
        if len(v) > 128:
            raise ValueError("A senha deve ter no máximo 128 caracteres.")
        return v
    
# Resposta do login.
# A senha nunca deve sair na resposta.
class LoginResponse(BaseModel):
    access_token: str
    token_type: str
# Signup:
# - entrada: dados do novo usuario
# - saida: dados do usuario criado
class SignUpRequest(BaseModel):
    email: EmailStr = Field(..., max_length=255)
    senha: str
    loja: str = Field(..., min_length=1, max_length=100)
    business: bool = True
    whatsapp: str | None = None
    

    @field_validator("email")
    @classmethod
    def normalizar_email(cls, v):
        return v.strip().lower()

    @field_validator("senha")
    @classmethod
    def validar_senha(cls, v):
        if len(v) < 6:
            raise ValueError("A senha deve ter pelo menos 6 caracteres.")
        if len(v) > 128:
            raise ValueError("A senha deve ter no máximo 128 caracteres.")
        return v
# Resposta do cadastro.
# Deve refletir o que o banco gerou automaticamente.
class SignUpResponse(BaseModel):
    email: EmailStr 
    loja: str 
    business: bool
    whatsapp: str | None = None
    criado_em: datetime
    expira_em: datetime

# Tarefas futuras para este modulo:
# - remover duplicacao dos validadores de email e senha
# - criar um schema base compartilhado entre login e signup
# - padronizar mensagens de erro para o frontend
# - adicionar suporte a senha com hash quando o fluxo estiver maduro
# - separar auth em arquivos proprios se o modulo crescer
