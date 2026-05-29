# Testes automatizados do modulo de produtos.
#
# Casos minimos:
# - produto enviado com sucesso
# - validacao de campos obrigatorios
# - persistencia no banco
# - falha de banco tratada corretamente
#

def test_create_product(client):
    payload = {
        "nome": "Leite",
        "validade": "2024-12-31",
        "quantidade": 2,
        "ean": "1234567890123",
        "troca": True,
        "categoria": "Laticínios"
    }
    response = client.post("/products/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == payload["nome"]
    assert data["validade"] == payload["validade"]
    assert data["quantidade"] == payload["quantidade"]
    assert data["ean"] == payload["ean"]
    assert data["troca"] == payload["troca"]
    assert data["categoria"] == payload["categoria"]
def test_list_products(client):
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_update_product(client):
    create_payload = {
        "nome": "Iogurte",
        "validade": "2024-11-30",
        "quantidade": 1,
        "ean": "9876543210987",
        "troca": False,
        "categoria": "Laticínios"
    }
    create_response = client.post("/products/", json=create_payload)
    product_id = create_response.json()["id"]
    update_payload = {
        "validade": "2024-12-15",
        "quantidade": 3
    }
    response = client.put(f"/products/{product_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["validade"] == update_payload["validade"]
    assert data["quantidade"] == update_payload["quantidade"]

def test_delete_product(client):

    payload = {
        "nome": "Produto Delete",
        "validade": "2026-06-10",
        "quantidade": 5,
        "troca": False,
        "ean": "111111111",
        "categoria": "Teste"
    }

    create_response = client.post(
        "/products/",
        json=payload
    )

    product_id = create_response.json()["id"]

    response = client.delete(
        f"/products/{product_id}"
    )

    assert response.status_code == 200

    list_response = client.get("/products/")

    products = list_response.json()

    ids = [product["id"] for product in products]

    assert product_id not in ids
# Proximo passo:
# - criar testes do endpoint de produto real
# - usar a mesma estrategia de fixtures do auth
# - garantir limpeza dos dados de teste ao final
