from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Backend RAG funcionando"}

@app.post("/chat")
def chat_endpoint(message: dict):
    # Aquí irá la lógica del chatbot
    return {"response": f"Echo: {message.get('question', '')}"} 