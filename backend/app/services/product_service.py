# Regras de negocio dos produtos.
from sqlalchemy.orm import Session

from app.models.product import ValidadeDB
from app.models.product_catalog import ProductCatalogDB
from app.schemas.product import ProductCreate, ProductUpdate
# Aqui deve ficar a logica que fala com o banco.
# Esta camada e o ponto certo para receber o usuario_id ja resolvido pelo auth.
# O service nao deve depender do frontend para saber quem e o dono do produto.

#responsavel por criar produto no catalogo
def create_product(db: Session, payload: ProductCreate, usuario_id: int):
    catalog_product = db.query(ProductCatalogDB).filter(
        ProductCatalogDB.ean == payload.ean
    ).first()
    if catalog_product is None:

        new_catalog_product = ProductCatalogDB(
            nome=payload.nome,
            ean=payload.ean,
            troca=payload.troca,
            categoria=payload.categoria
        )
        db.add(new_catalog_product)

        db.commit()

        db.refresh(new_catalog_product)

        return new_catalog_product
    else:
        return catalog_product
#responsavel por criar um produto no registro operacional validade
def create_validade(db: Session, payload: ProductCreate, usuario_id: int):

        new_validade = ValidadeDB(
            nome=payload.nome,
            validade=payload.validade,
            quantidade=payload.quantidade,
            ean=payload.ean,
            troca=payload.troca,
            categoria=payload.categoria,
            usuario_id=usuario_id
        )
        db.add(new_validade)

        db.commit()

        db.refresh(new_validade)

        return new_validade

#catalog_product = produto unico no catalogo, validade_product = produto do registro operacional, pode ter repetidos e ser deletado quando o produto for consumido ou descartado.


def list_products(db: Session, usuario_id: int):
    products = db.query(ValidadeDB).filter(ValidadeDB.usuario_id == usuario_id, ValidadeDB.deletado == False).all()
    return products


def update_product(
    db: Session,
    product_id: int,
    payload: ProductUpdate,
    usuario_id: int
):

    product = db.query(ValidadeDB).filter(
        ValidadeDB.id == product_id,
        ValidadeDB.usuario_id == usuario_id,
        ValidadeDB.deletado == False
    ).first()

    if product is None:
        raise ValueError("Produto não encontrado")

    product.validade = payload.validade
    product.quantidade = payload.quantidade

    db.commit()

    db.refresh(product)

    return product
     
def delete_product(db:Session, product_id: int, usuario_id: int):
     product = db.query(ValidadeDB).filter(ValidadeDB.id == product_id, ValidadeDB.usuario_id == usuario_id).first()
     if product is None:
        raise ValueError("Produto não encontrado")
     product.deletado = True
     db.commit()
     return {"message": "Produto deletado com sucesso"}