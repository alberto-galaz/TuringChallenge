# Turing Challenge - Chatbot RAG + Ejecución de Código + Imágenes

Este proyecto es un sistema fullstack de chatbot con memoria dinámica, RAG (Retrieval-Augmented Generation), ejecución de código Python bajo demanda y soporte para imágenes extraídas de PDFs.

## Requisitos
- Docker y Docker Compose (recomendado)
- Python 3.11+ (si quieres correr el backend sin Docker)
- Node.js 18+ (si quieres correr el frontend sin Docker)

## Estructura del proyecto
```
Turing_Challenge/
  back/           # Backend FastAPI (RAG, memoria, ejecución de código, imágenes)
    data/         # PDFs fuente
    images/       # Imágenes extraídas de los PDFs (se genera en la ingesta)
    faiss_index/  # Base vectorial FAISS (se genera en la ingesta)
    service/      # Routers y lógica modular
    ingest.py     # Script de ingesta y extracción
    main.py       # Entry point FastAPI
    requirements.txt
  front/          # Frontend React
    src/components/Chatbot.js
    ...
  config.yaml     # Configuración de credenciales y parámetros
  docker-compose.yml
  README.md
```

## Primer uso: instalación y arranque

### 1. Clona el repositorio y entra en la carpeta
```bash
git clone <repo-url>
cd Turing_Challenge
```

### 2. Coloca tus PDFs en `back/data/`
- Pon los archivos PDF que quieras indexar en la carpeta `back/data/`.

### 3. Configura credenciales y parámetros
- Edita `config.yaml` para poner tu API key de Groq, modelo, umbrales, etc.

### 4. (Opcional) Instala dependencias manualmente
Si no usas Docker:
```bash
cd back
pip install -r requirements.txt
cd ../front
npm install
```

### 5. Arranca todo con Docker Compose
```bash
docker compose up --build
```
- El primer arranque puede tardar (ingesta de PDFs, creación de FAISS, extracción de imágenes).
- Si quieres forzar la ingesta de nuevo (por ejemplo, tras cambiar los PDFs), borra `back/faiss_index/` y `back/images/` antes de arrancar.

### 6. Accede al frontend
- Abre [http://localhost:3000](http://localhost:3000) en tu navegador.

## ¿Cómo funciona?
- El chatbot responde usando un modelo LLM (Groq/Llama3) y, si la pregunta es relevante para los PDFs, usa RAG para dar contexto documental.
- Si la pregunta requiere código Python, el modelo lo genera y el backend lo ejecuta de forma segura, devolviendo el resultado.
- Si el contexto relevante tiene una imagen asociada (extraída del PDF), el backend la devuelve y el frontend la muestra.
- Puedes preguntar por imágenes por contexto o por nombre de archivo (ej: "dame la imagen 400_square_degrees_cluster.pdf_p2_0").
- El sistema tiene memoria dinámica: cuando el historial supera el umbral de tokens, se resume automáticamente.

## Ejemplos de uso
- "¿Qué dice el PDF sobre clusters de galaxias?"
- "¿Puedes mostrarme la imagen de la página 2 del PDF sobre clusters de estrellas?"
- "Dame la imagen 400_square_degrees_cluster.pdf_p2_0"
- "Calcula la suma de los primeros 10 números naturales con código Python"

## Notas
- Las carpetas `back/images/` y `back/faiss_index/` están en el `.gitignore` y no se suben al repo.
- Si tienes problemas con la ingesta o las imágenes, revisa los logs del backend para errores.
- El frontend muestra emojis de transparencia (📚 para RAG, 💬 para solo modelo) y de "pensando" (🤔).

## Créditos
- Basado en FastAPI, LangChain, FAISS, HuggingFace, React, Groq Cloud.
