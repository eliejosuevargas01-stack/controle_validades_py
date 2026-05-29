/*
 * Arquivo: main.jsx
 * Objetivo: Ponto de montagem da aplicação React na DOM do HTML.
 *
 * O que fazer aqui:
 * - Importar o React e o ReactDOM.
 * - Importar os estilos globais (`import './styles/globals.css'`).
 * - Chamar `ReactDOM.createRoot(document.getElementById('root')).render(...)` passando o `<App />`.
 */
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './styles/globals.css'

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
)
