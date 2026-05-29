# Rotas do modulo de produtos.
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.services.product_service import create_product, create_validade, list_products, update_product, delete_product
from app.core.dependencies import get_current_user
from app.models.user import UserDB


router = APIRouter(prefix="/products", tags=["products"])


@router.post(
        "/",
          response_model=ProductResponse,
         status_code=status.HTTP_201_CREATED
         )

def create_product_route(payload: ProductCreate, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    try:
        create_product(db, payload=payload, usuario_id=current_user.id)
        validade = create_validade(db, payload=payload, usuario_id=current_user.id) 

        return validade
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    

@router.get("/", response_model=list[ProductResponse])
def list_products_route(db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    products = list_products(db=db, usuario_id=current_user.id)
    return products

@router.put("/{product_id}", response_model=ProductResponse)
def update_product_route(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    try:
        product = update_product(db=db, product_id=product_id, payload=payload, usuario_id=current_user.id)
        return product
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )

@router.delete("/{product_id}")
def delete_product_route(product_id: int, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    try:
        result = delete_product(db=db, product_id=product_id, usuario_id=current_user.id)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )

# Este arquivo deve receber os endpoints que o frontend vai chamar.
# A rota deve receber o payload do produto e delegar a persistencia para o service.
# O usuario_id nao deve ser confiado vindo do frontend; o ideal e resolver isso fora da rota.
#
# Proximo passo:
# - criar o router de produtos
# - adicionar a rota de envio/criacao de produto
# - ligar o service de produto
# - depois criar uma rota de sugestao usando ean ou nome para buscar no catalogo fixo
#
# Tarefas futuras:
# - separar rotas por operacao se o modulo crescer
# - adicionar endpoints de listagem e edicao
# - padronizar respostas de erro e sucesso