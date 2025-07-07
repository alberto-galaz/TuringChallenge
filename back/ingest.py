import os
import sys
import warnings
import base64

# Silenciar warnings molestos de PyMuPDF
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import fitz  # PyMuPDF

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
VECTOR_DB_PATH = os.path.join(os.path.dirname(__file__), 'faiss_index')
INDEX_FILE = os.path.join(VECTOR_DB_PATH, 'index.faiss')
IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'images')
os.makedirs(IMAGES_DIR, exist_ok=True)

# 1. Extraer texto y asociar imágenes por página
def load_pdfs_with_images(data_dir):
    docs = []
    for fname in os.listdir(data_dir):
        if fname.lower().endswith('.pdf'):
            loader = PyPDFLoader(os.path.join(data_dir, fname))
            pdf_docs = loader.load()
            # Extraer imágenes por página
            pdf_path = os.path.join(data_dir, fname)
            doc = fitz.open(pdf_path)
            page_images = {}
            for page in doc:
                images = []
                for i, img in enumerate(page.get_images(full=True)):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image['image']
                    image_ext = base_image['ext']
                    image_filename = f"{fname}_p{page.number}_{i}.{image_ext}"
                    image_path = os.path.join(IMAGES_DIR, image_filename)
                    with open(image_path, 'wb') as f:
                        f.write(image_bytes)
                    images.append(image_path)
                if images:
                    page_images[page.number] = images
            # Asociar imágenes a los documentos por página
            for d in pdf_docs:
                page_num = d.metadata.get('page', None)
                if page_num is not None and page_num in page_images:
                    # Solo asociar la primera imagen de la página (puedes extender a varias)
                    d.metadata['image_path'] = page_images[page_num][0]
                docs.append(d)
    return docs

# 3. Ejemplo de extracción estructurada (nombre, apellidos, fecha nacimiento)
def extract_structured_info(text):
    import re
    info = {}
    patterns = {
        'nombre': r'Nombre\s*:\s*(.*)',
        'apellidos': r'Apellidos\s*:\s*(.*)',
        'fecha_nacimiento': r'Fecha de nacimiento\s*:\s*(.*)'
    }
    for key, pat in patterns.items():
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            info[key] = m.group(1).strip()
    return info

# 4. Ingesta principal (texto y vectorización)
def ingest():
    if os.path.exists(INDEX_FILE):
        print(f"[INGEST] Índice FAISS ya existe en {INDEX_FILE}, omitiendo ingesta de PDFs.")
        return
    print("Iniciando ingesta de PDFs...")
    docs = load_pdfs_with_images(DATA_DIR)
    print(f'PDFs cargados: {len(docs)}')
    all_text = '\n'.join([d.page_content for d in docs])
    structured = extract_structured_info(all_text)
    if structured:
        print('Información estructurada encontrada:', structured)
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = splitter.split_documents(docs)
    # Los metadatos de image_path se mantienen en los splits
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.from_documents(texts, embeddings)
    db.save_local(VECTOR_DB_PATH)
    print('Vector DB guardada en', VECTOR_DB_PATH)
    # Contar imágenes guardadas
    num_images = len([f for f in os.listdir(IMAGES_DIR) if f.lower().endswith(('png','jpg','jpeg'))])
    print(f'Imágenes guardadas: {num_images}')
    return structured, num_images 