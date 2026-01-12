from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import transactions,assistant
from app.db import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Transacciones")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transactions.router, prefix="/transactions",tags=["Transactions"])
app.include_router(assistant.router, prefix="/assistant", tags=["Assistant"])

@app.get("/")
def root():
    return {"message": "API Online"}