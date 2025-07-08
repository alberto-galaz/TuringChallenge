# app.py
"""
Chatbot RAG sencillo con React, LangChain y FAISS
"""

# 1. Importar librerías necesarias
# 2. Definir función para cargar y procesar PDFs
# 3. Crear o cargar base de datos vectorial FAISS
# 4. Definir función de búsqueda y generación de respuesta
# 5. Configurar interfaz React

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import camelot
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    pass