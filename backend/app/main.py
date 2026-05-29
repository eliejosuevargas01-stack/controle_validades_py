from fastapi import FastAPI

# - importar o router de auth quando ele estiver pronto
from app.routers.auth import router as auth_router
from app.db.init_db import init_db
from app.routers.products import router as products_router
from fastapi.middleware.cors import CORSMiddleware
# Ponto de entrada principal da API.
# Aqui a app FastAPI nasce e depois recebe os routers.
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Próximo passo:

# - usar `app.include_router(...)`

app.include_router(auth_router)
app.include_router(products_router)
# - manter a lógica de login fora deste arquivo


@app.on_event("startup")
def startup_event():
    # Cria as tabelas faltantes no banco quando a API sobe.
    # Assim o catalogo fixo de produtos entra sem precisar escrever SQL manualmente.
    init_db()