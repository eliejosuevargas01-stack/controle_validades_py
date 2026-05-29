from datetime import date

from pydantic import BaseModel, Field, ConfigDict


# Schemas do modulo de produtos.
# Aqui ficam os dados que o frontend envia e o que a API devolve.
# O usuario_id nao entra no payload do frontend.
# Ele sera preenchido pelo backend na camada de service quando o usuario autenticado for conhecido.


class ProductCreate(BaseModel):
    nome: str = Field(..., min_length=1, max_length=255)
    validade: date
    quantidade: int = Field(..., ge=0)
    troca: bool = False
    ean: str = Field(..., min_length=1, max_length=50)
    categoria: str = Field(..., min_length=1, max_length=100)

class ProductResponse(BaseModel):
    model_config = ConfigDict(from_atributes=True)
    id: int
    nome: str
    validade: date
    quantidade: int
    troca: bool
    ean: str 
    categoria: str 

class ProductUpdate(BaseModel):
    validade: date
    quantidade: int = Field(..., ge=0)
# Tarefas futuras para este modulo:
# - ligar cada produto ao usuario autenticado via usuario_id no banco
# - separar schemas de create, update e response se o modulo crescer
# - adicionar validacoes de ean e regras de negocio por categoria
# - definir quais campos sao obrigatorios na insercao e quais sao opcionais
# - alinhar os nomes dos campos com o banco, se o frontend e a tabela usarem outro padrao
