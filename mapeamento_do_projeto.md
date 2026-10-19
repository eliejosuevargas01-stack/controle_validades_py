# Mapeamento do Projeto: Controle de Validades

## Visão Geral
O projeto "Controle de Validades" é um sistema criado para organizar a rotina de supermercados e acompanhar os vencimentos de produtos de forma a apoiar a retirada deles no momento certo. O sistema foi originado no n8n (com persistência em PostgreSQL) e vem sendo evoluído em Python (FastAPI) e React, mantendo a estrutura antiga (legada) enquanto o novo frontend é desenvolvido.

### Tecnologias Utilizadas
- **Frontend:** React, Vite, React Router DOM, Vitest.
- **Frontend Legado:** HTML/CSS/JS simples (mantendo integração com n8n).
- **Backend:** Python, FastAPI, SQLAlchemy, PostgreSQL.
- **Testes:** pytest (backend), vitest (frontend react), node (frontend legado).

---

## 1. Frontend

O frontend está dividido em duas áreas dentro da pasta `frontend/`:

### 1.1 React App (`frontend/react_app/`)
Esta é a nova interface em desenvolvimento utilizando Vite e React.
- **Componentes:** Localizados em `src/components/` (Input, Button, Navbar, ProtectedRoute).
- **Páginas:** Localizadas em `src/pages/` (Login, Register, Products, Dashboard).
- **Serviços (`src/services/`):**
  - `authService.js`: Comunicação com o backend para autenticação (login, signup, token management).
  - `productService.js`: Operações de CRUD para produtos (`createProduct`, `getProducts`, `updateProduct`, `deleteProduct`).
- **Roteamento:** Configurado no arquivo raiz `App.jsx` com suporte a autenticação (ProtectedRoute).

### 1.2 Legacy App (`frontend/legacy_app/`)
Este diretório acomoda todo o código original em HTML/CSS/JS, que ainda se integra com webhooks do n8n.
- Contém páginas como `index.html`, `login.html`, `checkout.html`, etc.
- A suite de testes antiga foi movida para cá (`scripts/run-tests.mjs` e arquivos na pasta `tests/`).

---

## 2. Backend (`backend/`)

O backend é uma API feita em FastAPI que gerencia autenticação, produtos e banco de dados.

### 2.1 Estrutura do Backend (`backend/app/`)
- **`main.py`**: Ponto de entrada da aplicação, onde os roteadores (`auth_router` e `products_router`) são anexados ao FastAPI, além da criação e inicialização do banco (`init_db`).
- **Configuração de Banco de Dados (`db/`)**:
  - `session.py` configura o `engine` do SQLAlchemy, utilizando a conexão com o PostgreSQL via `DATABASE_URL`.
- **Modelos (`models/`)**:
  - A principal tabela é mapeada pela classe `ValidadeDB` (`product.py`) (com alias temporário `ProductDB`). Essa tabela guarda dados essenciais do usuário e de cada produto lançado.
- **Roteadores (`routers/`)**:
  - `auth.py`: Controla o login e o registro (signup) utilizando o service `auth_service`.
  - `products.py`: Controla as rotas CRUD de produtos (criação, listagem, atualização, exclusão).
- **Schemas (`schemas/`)**:
  - `product.py`: Define os contratos Pydantic para comunicação de entrada (ex: `ProductCreate`) e saída (ex: `ProductResponse`).
  - `auth.py`: Semelhante, mas para autenticação e registro.

---

## 3. Testes
O projeto possui suites de testes bem definidas para suas camadas:
- **Frontend React:** Testes sendo executados via Vitest (`npm run test`).
- **Frontend Legado:** Scripts customizados (`node scripts/run-tests.mjs`).
- **Backend:** Testes presentes em `backend/tests/` utilizando Pytest.

---
*Este documento reflete a estrutura atual mapeada do repositório, indicando como os componentes se conectam para suprir as necessidades de controle de vencimento dos produtos.*