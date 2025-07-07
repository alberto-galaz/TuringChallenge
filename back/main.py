from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from service.chat_router import chat_router
from service.execute_router import execute_router

app = FastAPI()

# Permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(execute_router)

@app.get("/")
def read_root():
    return {"message": "Backend RAG funcionando"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 