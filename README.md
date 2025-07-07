# Turing Challenge RAG Chatbot

## Requisitos
- [Docker](https://www.docker.com/) y [Docker Compose](https://docs.docker.com/compose/)

## Cómo levantar el proyecto

1. Clona este repositorio
2. Ejecuta:
   ```bash
   docker-compose up --build
   ```
3. El frontend estará disponible en [http://localhost:3000](http://localhost:3000)
4. El backend (API) estará en [http://localhost:8000](http://localhost:8000)

## Estructura
- `front/`: React (chatbot)
- `back/`: FastAPI + LangChain (RAG)

## Notas
- Los PDFs deben ir en `back/data/`
- Puedes modificar el código y reiniciar los servicios con `docker-compose up --build`
