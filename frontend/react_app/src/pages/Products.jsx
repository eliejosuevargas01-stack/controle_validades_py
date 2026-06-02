/*
 * Arquivo: Products.jsx
 * Objetivo: Página de listagem, visualização e gestão dos produtos cadastrados.
 *
 * O que fazer aqui:
 * - Exibir uma tabela ou lista com os dados do formato ProductResponse:
 *   (ID, Nome, Validade, Quantidade, Troca, EAN, Categoria).
 *
 * - Criar um formulário (pode ser num Modal ou na mesma tela) que obedeça ao payload ProductCreate:
 *   - Nome: Input texto (obrigatório, max 255 chars).
 *   - Validade: Input de data.
 *   - Quantidade: Input numérico (obrigatório, não pode ser menor que 0).
 *   - Troca: Input checkbox/boolean (padrão falso).
 *   - EAN: Input texto (obrigatório, código de barras).
 *   - Categoria: Input texto/select (obrigatório).
 *
 * - Integrar os botões de ação para chamar list(), create(), edit() e delete() do productService.
 */
import { useEffect, useState } from "react"

import {
  getProducts,
  createProduct,
  deleteProduct,
  updateProduct
} from "../services/productService"

function getDiasRestantes(validade) {
  const hoje = new Date()
  const vencimento = new Date(validade)
  const diferenca =
  vencimento - hoje
  return Math.ceil(
    diferenca / (1000 * 60 * 60 * 24)
  )
}

function getStatusValidade(validade) { 
  const dias = getDiasRestantes(validade)
  if (dias < 0)
    return "VENCIDO"
  if (dias <= 3)
    return "CRITICO"
  if (dias <= 7)
    return "ATENÇÃO"
  if (dias <= 30)
    return "PRÓXIMO"
  return "OK"
}
function formatDate(data) {
  return new Date(data).toLocaleDateString("pt-BR")
}

function Products() {

  const [products, setProducts] = useState([])

  const [formData, setFormData] = useState({
    nome: "",
    validade: "",
    quantidade: 0,
    troca: false,
    ean: "",
    categoria: ""
  })

const [editingProductId, setEditingProductId] = useState(null)

const [pendingProducts, setPendingProducts] = useState([])

  async function loadProducts() {

    try {

      const data = await getProducts()

      setProducts(data)

    } catch (error) {

      console.error(error)

    }
  }

  useEffect(() => {

    loadProducts()

  }, [])

function handleEdit(product) {

  setEditingProductId(product.id)

  setFormData({
    nome: product.nome,
    validade: product.validade,
    quantidade: product.quantidade,
    troca: product.troca,
    ean: product.ean,
    categoria: product.categoria
  })
}

function handleAddProduct() {

  if (
  !formData.nome.trim() ||
  !formData.validade ||
  !formData.ean.trim() ||
  !formData.categoria.trim()
) {
  alert("Preencha todos os campos obrigatórios.")
  return
}

  setPendingProducts([
    ...pendingProducts,
    formData
  ])

  setFormData({
    nome: "",
    validade: "",
    quantidade: 0,
    troca: false,
    ean: "",
    categoria: ""
  })
}

  function handleChange(event) {

    const { name, value } = event.target

    setFormData({
      ...formData,
      [name]: value
    })
  }

 async function handleSubmit(event) {

  event.preventDefault()

  try {

    if (editingProductId) {

      await updateProduct(
        editingProductId,
        formData
      )

      setEditingProductId(null)

    } else {
      if (pendingProducts.length > 0) {
        for (const product of pendingProducts) {
          await createProduct(product)
        }
        setPendingProducts([])
      } else {
        await createProduct(formData)
      }
    }

    await loadProducts()

    setFormData({
      nome: "",
      validade: "",
      quantidade: 0,
      troca: false,
      ean: "",
      categoria: ""
    })

  } catch (error) {

    console.error(error)

  }
}
  async function handleDelete(productId) {

    try {

      await deleteProduct(productId)

      await loadProducts()

    } catch (error) {

      console.error(error)

    }
  }

  async function handleSaveAll() {
    try {
      if (pendingProducts.length === 0) {
        alert ("Nenhum produto na lista.")
        return
      }

      for (const product of pendingProducts) {
        await createProduct(product)
      }
      setPendingProducts([])
      await loadProducts()
      alert("Produtos cadastrados com sucesso!")
    } catch (error) {
      console.error(error)
    }
  }

  return (

    <div className="products-page">

      <h1>Controle de Produtos</h1>

      <form onSubmit={handleSubmit}>

        <input
          type="text"
          name="nome"
          placeholder="Nome"
          value={formData.nome}
          onChange={handleChange}
        />

        <input
          type="date"
          name="validade"
          value={formData.validade}
          onChange={handleChange}
        />

        <input
          type="number"
          name="quantidade"
          placeholder="Quantidade"
          value={formData.quantidade}
          onChange={handleChange}
        />

        <input
          type="text"
          name="ean"
          placeholder="EAN"
          value={formData.ean}
          onChange={handleChange}
        />

        <input
          type="text"
          name="categoria"
          placeholder="Categoria"
          value={formData.categoria}
          onChange={handleChange}
        />

        <button type="submit">
          {editingProductId ? "Salvar" : 
          pendingProducts.length > 0 ? 
          `Cadastrar Todos (${pendingProducts.length})`:
          "Cadastrar"}
        </button>
        <button
                type="button"
                onClick={handleAddProduct}>
                  Adicionar à Lista
                </button>
      </form>

      <hr />

      <h2>Produtos Pendentes</h2>
      <ul>
        {pendingProducts.map((product, index) => (
          <li key={index}>
            {product.nome}
            {" - "}
            {product.quantidade}
            {" unidades"}
          </li>
        ))}
      </ul>
      <table>

        <thead>

          <tr>
            <th>ID</th>
            <th>Nome</th>
            <th>Validade</th>
            <th>Quantidade</th>
            <th>Dias Restantes</th>
            <th>Status</th>
            <th>Ações</th>
          </tr>

        </thead>

        <tbody>

          {products.map(product => (

            <tr key={product.id}>

              <td>{product.id}</td>

              <td>{product.nome}</td>

              <td>{formatDate(product.validade)}</td>

              <td>{product.quantidade}</td>

              <td>
                {getDiasRestantes(product.validade)}
              </td>

              <td>
                {getStatusValidade(product.validade)}
              </td>

              <td>

                <button
                  onClick={() => handleDelete(product.id)}
                >
                  Deletar
                </button>
                <button
                    onClick={() => handleEdit(product)}
                >
                    Editar
                </button>
                
              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>
  )
}

export default Products