/*
 * Arquivo: Register.jsx
 * Objetivo: Página para criação de uma nova conta de usuário.
 *
 * O que fazer aqui:
 * - Construir o formulário de cadastro com campos como nome, e-mail, senha e confirmação de senha.
 * - Fazer as validações de input.
 * - Ao confirmar, chamar o serviço de registro para salvar o novo usuário.
 */
import { useState } from "react" 

import { signup } from "../services/authService"

function Register() {
    const [nome, setNome] = useState("")
    const [email, setEmail] = useState("")
    const [senha, setSenha] = useState("")

    async function handleSubmit(event) {
        event.preventDefault()
        try { 
            const data = await signup({
                nome, 
                email, 
                senha

            })
            console.log(data)

            alert("Usuario registrado com sucesso")
            
        } catch (error) {
            console.error(error)
            alert ("Erro ao criar usuario")
        }
        
    }
    return (
        <div className="auth-container">
            <form
            className="auth-form"
            onSubmit={handleSubmit}>
                <h1>Criar conta</h1>
                <input 
                type="text"
                placeholder="Nome"
                value={nome}
                onChange={(e) => setNome(e.target.value)}
                />
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
                <button type="submit">
                Registrar
                </button>
            </form>
        </div>
    )
}
export default Register