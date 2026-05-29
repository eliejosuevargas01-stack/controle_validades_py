# Relatório Final de Reorganização do Frontend

## 1. Modificações Estruturais (Arquivos Movidos)

Todo o frontend foi reorganizado em duas pastas principais dentro de `frontend/`:
- `frontend/react_app/`: Onde foi colocado o aplicativo React desenvolvido.
- `frontend/legacy_app/`: Onde foi acomodado todo o código original HTML/CSS/JS (inclusive as pastas `assets`, `css`, e `js`).

A movimentação englobou:
- `frontend/repo-front-temp/legacy_app/*` -> `frontend/legacy_app/`
- `frontend/repo-front-temp/frontend/*` -> `frontend/react_app/`
- Além disso, os diretórios de testes (`tests` e `scripts`) pertencentes ao código da plataforma como um todo e com referências a arquivos antigos foram movidos para dentro de `frontend/legacy_app/` para preservar a estrutura de testes histórica conforme a diretiva de manter o legado funcional.

## 2. Arquivos Removidos
A pasta transitória que causava bagunça na importação foi inteiramente removida:
- `frontend/repo-front-temp/` (após tudo de dentro dela ser movido).
- `frontend/repo-front-temp/.gitignore` e `frontend/repo-front-temp/agent-prompt.md` que eram arquivos temporários sem ligação de código.

## 3. Imports Corrigidos e Tratados
Na suíte de testes legada movida de `scripts` e `tests` pro diretório `frontend/legacy_app/`, as referências aos caminhos para leitura dos arquivos foram corrigidas. Agora o código lê `js/main.js` ou caminha de volta para fora procurando os arquivos do `backend/app/main.py`.

Um erro de tipografia de linter foi corrigido também em `frontend/react_app/src/pages/Register.jsx` (troca de `classsName` para `className` e `setSesnha` para `setSenha`).

## 4. Dependências Removidas
Verificamos pelo `depcheck` que o react listava algumas dependências em desuso de testes. Foi cogitada a remoção, mas decidi devolvê-las ao sistema por orientação que eles seriam necessários num futuro de testes das rotas e componentes reescritos, evitando uma regressão.

---

# Explicação do Código React

Abaixo está o guia detalhado e a "tradução" dos principais arquivos de configuração e inicialização do projeto em React:

## `frontend/react_app/package.json`

O `package.json` é a carteira de identidade e o motor de um projeto Node/React. Ele dita os nomes, como iniciar os scripts e quais bibliotecas o projeto precisa para existir.

```json
{
  "name": "controle-de-validade-frontend", // Nome do seu projeto.
  "private": true,                         // Marca que o projeto não deve ser publicado publicamente no NPM.
  "version": "0.0.0",                      // Versão inicial do app.
  "type": "module",                        // Define que o código usa a sintaxe moderna (import/export) de JavaScript.

  "scripts": {
    "dev": "vite",                         // Comando para subir o servidor local (npm run dev).
    "build": "vite build",                 // Comando para empacotar o projeto para ir pro ar (produção).
    "lint": "eslint . --ext js,jsx ...",   // Comando que varre o código procurando por erros de digitação ou práticas ruins.
    "preview": "vite preview",             // Inicia um servidor local baseado na sua build pra você ver como ficou o pacote final.
    "test": "vitest run"                   // Roda os testes com a biblioteca de teste Vitest.
  },

  "dependencies": {
    "react": "^18.2.0",                    // O pacote principal do React, que permite criar componentes na tela.
    "react-dom": "^18.2.0",                // Ferramenta que junta o React com a árvore (DOM) de fato do navegador web.
    "react-router-dom": "^6.30.3"          // Gerenciador de links e "páginas" dentro de um app React de página única (SPA).
  },

  "devDependencies": {
    // Bibliotecas usadas *apenas* pelo desenvolvedor para testar ou empacotar a aplicação, e que não vão pesar no tamanho final pro usuário final.
    "vite": "^5.0.8",                      // Servidor rápido usado no comando "dev".
    "eslint": "^8.55.0",                   // Avaliador de qualidade e padrão do código.
    "vitest": "^4.1.7",                    // Usado em "test" para garantir que suas funções rodem sem erro.
    "@testing-library/react": "^16.3.2"    // Lib de teste focada em renderizar o componente como se fosse o usuário e checar o que apareceu.
  }
}
```

## `frontend/react_app/vite.config.js`

Este arquivo dita como o Vite vai preparar o código para rodar local e em produção. O Vite é o substituto do "Webpack", focado em velocidade absurda.

```javascript
import { defineConfig } from 'vite'        // Traz a função do Vite que ajuda o editor a dar autocompletar na configuração.
import react from '@vitejs/plugin-react'   // Importa o plugin oficial pra ele saber compilar coisas com cara de React (.jsx)

// Define e exporta o bloco de regras do Vite
export default defineConfig({
  plugins: [react()],                      // Avisa "ei Vite, nós vamos usar React aqui, prepare os carregadores corretos."
})
```

## `frontend/react_app/src/main.jsx`

Esse arquivo é a ponte entre todo o seu código JS (o App) e o navegador em branco (`index.html`).

```javascript
import React from 'react'                     // Importa o núcleo principal do React.
import ReactDOM from 'react-dom/client'       // Importa a biblioteca para desenhar algo na tela (Web).
import App from './App.jsx'                   // Chama o seu componente pai/central do seu site inteiro (o App).
import './styles/globals.css'                 // Puxa as regras de design CSS que vão se aplicar no site todo.

// Ele pega uma div em branco chamada "root" que está lá no seu index.html,
// Inicializa o gerenciador da raíz do React nela,
// e então joga o conteúdo do componente `<App />` lá dentro.
// O `<React.StrictMode>` é um vigia que força o React em ambiente dev a testar seu app em busca de lixo de código.
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

## `frontend/react_app/src/App.jsx`

O App.jsx é o coordenador geral do seu projeto, onde as rotas e o coração visual batem. É daqui que o usuário será empurrado para a tela de Login ou Produtos dependendo da URL que ele acessou.

```javascript
// Importa 3 coisas cruciais pra navegação:
// BrowserRouter: Cobre o App para habilitar detecção da barra de URL
// Routes: A caixa onde ficam todas as rotas possíveis.
// Route: O item específico de cada Rota.
import {
    BrowserRouter,
    Routes,
    Route
} from "react-router-dom"

// Puxa as "páginas" do site, que na verdade são só componentes visuais que preenchem a tela toda
import Products from "./pages/Products"
import Login from "./pages/Login"
import Register from "./pages/Register"

// Declara a função do componente principal.
function App() {
    return (
        <BrowserRouter>             {/* Habilita as URLs do tipo site.com/produtos funcionarem. */}
            <Routes>                {/* Abre o painel controlador de rotas */}

                {/* Quando a URL for "/", renderize o componente Products. */}
                <Route
                path="/"
                element={<Products />}/>

                {/* Quando a URL for "/products", também renderiza Products. */}
                <Route
                path="/products"
                element={<Products />}/>

                {/* Quando a URL for "/login", mostra o formulário de Login. */}
                <Route
                path="/login"
                element={<Login />}/>

                {/* Quando a URL for "/Register", mostra o formulário de Cadastro. */}
                <Route
                path="/Register"
                element={<Register />}/>

            </Routes>
        </BrowserRouter>
    )
}

export default App  // Permite que outros arquivos (como o main.jsx ali em cima) importem essa estrutura inteira.
```