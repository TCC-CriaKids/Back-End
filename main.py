from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.api import api_router

app = FastAPI(title="CRIA Kids")

origins = [
    "https://cria-kids-tcc.vercel.app",
    "http://127.0.0.1:5500",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas com prefixo /api
app.include_router(api_router)
