# Turing Challenge - Chatbot RAG + Ejecución de Código + Imágenes

Este proyecto es un sistema fullstack de chatbot con memoria dinámica, RAG (Retrieval-Augmented Generation), ejecución de código Python bajo demanda y soporte para imágenes extraídas de PDFs.

## Requisitos
- Docker y Docker Compose (recomendado)
- Python 3.11+ (si quieres correr el backend sin Docker)
- Node.js 18+ (si quieres correr el frontend sin Docker)


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
