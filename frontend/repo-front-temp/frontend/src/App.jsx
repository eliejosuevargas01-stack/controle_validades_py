/*
 * Arquivo: App.jsx
 * Objetivo: Componente raiz da aplicação.
 *
 * O que fazer aqui:
 * - Este é o ponto de entrada principal do React.
 * - Envolver a aplicação com os Provedores de Contexto (ex: `<AuthProvider>`).
 * - Renderizar o componente de Rotas (`<AppRoutes />`).
 * - Evitar colocar regras de negócio pesadas aqui, delegando para as páginas ou contextos.
 */
import {
    BrowserRouter,
    Routes,
    Route
} from "react-router-dom"


import Products from "./pages/Products"
import Login from "./pages/Login"
import Register from "./pages/Register"


function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route
                path="/"
                element={<Products />}/>
                <Route
                path="/products"
                element={<Products />}/>
                <Route
                path="/login"
                element={<Login />}/>
                <Route
                path="/Register"
                element={<Register />}/>
            
            </Routes>
        </BrowserRouter>
    )
}

export default App