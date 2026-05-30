/*
 * Arquivo: Login.jsx
 * Objetivo: Página principal de autenticação do usuário.
 *
 * O que fazer aqui:
 * - Criar a estrutura visual da tela de login (formulário de e-mail e senha).
 * - Usar estados (com `useState`) para gerenciar os valores dos inputs.
 * - Integrar com o `AuthContext` ou chamadas de serviço (`authService`) para realizar a autenticação real ou simulada.
 * - Redirecionar o usuário para o `Dashboard` em caso de sucesso.
 */

import { useState } from "react"

import { login } from "../services/authService"

import { useNavigate } from "react-router-dom"


function Login() {
    const [email, setEmail] = useState("")
    const [senha, setSenha] = useState("")
    const navigate = useNavigate()
    async function handleSubmit(event) {
        event.preventDefault()
        try {
            const data = await login({
                email, 
                senha
            })
            console.log(data)
            navigate("/products")
        } catch (error) {
            console.error(error)
            alert("Erro ao fazer login")

        }
    }
    return (
        <div className="auth-container">
            <form
            className="auth-form"
            onSubmit={handleSubmit}
            >
                <h1>Login</h1>
                <input
  type="email"
  placeholder="Email"
  value={email}
  onChange={(e) => setEmail(e.target.value)}
  />

<input
  type="password"
  placeholder="Senha"
  value={senha}
  onChange={(e) => setSenha(e.target.value)}
  />
  <button type="submit">Entrar</button>
  </form>
        </div>
    )
}

export default Login












