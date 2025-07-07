import os
import yaml
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from ingest import ingest

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.yaml')
with open(CONFIG_PATH, 'r') as f:
    config = yaml.safe_load(f)

VECTOR_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'faiss_index')

embeddings = None
vector_db = None
rag_cfg = config['rag']
RAG_K = rag_cfg.get('k', 3)
RAG_DISTANCE_THRESHOLD = rag_cfg.get('distance_threshold', 0.3)

def init_rag():
    global embeddings, vector_db
    ingest()
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_db = FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)

def search_context(question, k=None, distance_threshold=None):
    if vector_db is None:
        return None
    k = k if k is not None else RAG_K
    distance_threshold = distance_threshold if distance_threshold is not None else RAG_DISTANCE_THRESHOLD
    results = vector_db.similarity_search_with_score(question, k=k)
    print(f"Scores de distancia para '{question}':", [score for doc, score in results])
    if not results or results[0][1] > distance_threshold:
        return {"context": None, "image_path": None}
    # Busca el primer doc con imagen asociada
    image_path = None
    for doc, score in results:
        if doc.metadata.get('image_path'):
            image_path = doc.metadata['image_path']
            break
    context = "\n".join([doc.page_content for doc, score in results if score <= distance_threshold])
    return {"context": context if context.strip() else None, "image_path": image_path} 