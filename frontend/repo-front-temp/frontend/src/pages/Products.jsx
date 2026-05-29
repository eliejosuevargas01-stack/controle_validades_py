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

      await createProduct(formData)

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
          {editingProductId ? "Salvar" : "Cadastrar"}
        </button>

      </form>

      <hr />

      <table>

        <thead>

          <tr>
            <th>ID</th>
            <th>Nome</th>
            <th>Validade</th>
            <th>Quantidade</th>
            <th>Ações</th>
          </tr>

        </thead>

        <tbody>

          {products.map(product => (

            <tr key={product.id}>

              <td>{product.id}</td>

              <td>{product.nome}</td>

              <td>{product.validade}</td>

              <td>{product.quantidade}</td>

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