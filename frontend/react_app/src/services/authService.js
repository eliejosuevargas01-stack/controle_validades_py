/*
 * Arquivo: authService.js
 * Objetivo: Centralizar as funções de comunicação com o backend referentes à autenticação.
 *
 * O que fazer aqui:
 * - O backend suporta atualmente as funcionalidades: signup e login.
 *
 * - Criar e exportar a função login(credenciais):
 *   Deve enviar o e-mail/usuário e senha para o endpoint de login.
 *   Salvar o token JWT ou sessão retornado no localStorage ou context.
 *
 * - Criar e exportar a função signup(dadosUsuario):
 *   Deve enviar os dados do novo usuário para o endpoint de registro.
 *
 * - Estas funções devem usar fetch ou axios para fazer as requisições HTTP e tratar possíveis erros (ex: credenciais inválidas).
 */
const API_URL = "http://localhost:8001/auth"

export async function signup(userData) {
    const response = await fetch(
        `${API_URL}/signup`,
        {
            method: "POST",
            headers: {
                "content-type": "application/json"
        },
            body: JSON.stringify(userData)
        }
    )
    if (!response.ok) {
            throw new Error("Erro ao registrar usuario")
    }
    return response.json()
        
    
}

export async function login(credentials) {
    const response = await fetch(
        `${API_URL}/login`,
        {method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(credentials)
        }
    )
    if (!response.ok) {
        throw new Error("Email ou senha invalidos")

    }

    const data = await response.json()
    localStorage.setItem(
        "token",data.access_token
    )
    return data
}

export function getToken() {
    return localStorage.getItem("token")
}

export function logout() {
    localStorage.removeItem("token")
}

export function isAuthenticated() {
    return !!localStorage.getItem("token")
}