import { getToken } from "./authService"
const API_URL = "http://localhost:8001/products"

export async function createProduct(productData) {

    const response = await fetch(API_URL, {
        method: "POST",
        headers: 
            getAuthHeaders(),
        body: JSON.stringify(productData)
    })

    if (!response.ok) {
        throw new Error("Erro ao criar produto")
    }

    return response.json()
}

export async function getProducts() {
const response = await fetch(API_URL, {headers: getAuthHeaders()})
if (!response.ok) {
    throw new Error("Erro ao buscar produtos")
}
return response.json()
}

export async function deleteProduct(productId) {
    const response = await fetch(
        `${API_URL}/${productId}`,
        {
            method: "DELETE",
            headers: getAuthHeaders()
        }
    )

    if (!response.ok) {
        throw new Error("Erro ao deletar produto")
    }

    return response.json()
}

export async function updateProduct(productId, productData) {
    const response = await fetch(`${API_URL}/${productId}`, {
        method: "PUT",
        headers: getAuthHeaders(),
        body: JSON.stringify(productData)
    })

    if (!response.ok) {
        throw new Error("Erro ao atualizar produto")
    }

    return response.json()
}
function getAuthHeaders() {
    return {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${getToken()}`
    }
}
/*
 * Arquivo: productService.js
 * Objetivo: Centralizar as requisições à API relacionadas aos produtos.
 * O que fazer aqui:
 * - O backend suporta: create, edit, delete, list.
 *
 * - Implementar função listProducts():
 *   Deve retornar uma lista de objetos ProductResponse:
 *   { id: int, nome: string, validade: string(date), quantidade: int, troca: bool, ean: string, categoria: string }
 *
 * - Implementar função createProduct(data):
 *   O payload esperado (ProductCreate) deve ser:
 *   {
 *     nome: string (1 a 255 chars),
 *     validade: string (formato YYYY-MM-DD),
 *     quantidade: int (maior ou igual a 0),
 *     troca: boolean (padrão false),
 *     ean: string (1 a 50 chars),
 *     categoria: string (1 a 100 chars)
 *   }
 *
 * - Implementar updateProduct(id, data): Recebe o ID e o payload ProductCreate modificado.
 * - Implementar deleteProduct(id): Envia requisição para excluir o produto.
 */
