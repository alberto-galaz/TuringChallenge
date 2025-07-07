from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
import requests
from service.model import GROQ_API_KEY, GROQ_API_URL, GROQ_MODEL
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
import yaml
import os

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.yaml')
with open(CONFIG_PATH, 'r') as f:
    config = yaml.safe_load(f)

MAX_TOKENS_HISTORY = config['memory']['max_tokens_history']

conversation_memory = ConversationBufferMemory(return_messages=True)
conversation_summary = None

def init_memoria():
    global conversation_summary
    llm = ChatOpenAI(openai_api_key=GROQ_API_KEY, base_url=GROQ_API_URL, model=GROQ_MODEL)
    conversation_summary = ConversationSummaryMemory(llm=llm, return_messages=True)

def count_tokens():
    # Solo cuenta palabras de mensajes con contenido real
    history = " ".join([
        m.content for m in conversation_memory.buffer if m.content.strip()
    ])
    tokens = len(history.split())
    print(f"[TOKENS] Historial actual tiene {tokens} tokens")
    return tokens

def summarize_history(history):
    prompt = (
        "Resume la siguiente conversación de forma breve y clara, manteniendo los puntos importantes y el contexto relevante para continuar la charla:\n\n" + history
    )
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "Eres un asistente que resume conversaciones manteniendo el contexto importante."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 120,
        "temperature": 0.3
    }
    response = requests.post(GROQ_API_URL, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()
    resumen = result["choices"][0]["message"]["content"]
    return resumen

def log_memoria_estado():
    print("[MEMORIA] Estado actual del buffer:")
    for i, m in enumerate(conversation_memory.buffer):
        print(f"  [{i}] {m}") 