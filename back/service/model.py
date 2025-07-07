import requests
import yaml
import os

# Cargar configuración
CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.yaml')
with open(CONFIG_PATH, 'r') as f:
    config = yaml.safe_load(f)

groq_cfg = config['groq']
GROQ_API_URL = groq_cfg['api_url']
GROQ_API_KEY = groq_cfg['api_key']
GROQ_MODEL = groq_cfg['model']

SYSTEM_PROMPT = (
    "Eres un asistente experto. "
    "Si el usuario te pide explícitamente que resuelvas algo con código Python, "
    "genera el código necesario y enciérralo entre bloques triple backtick (```python ... ```). "
    "No expliques el código a menos que el usuario lo pida. "
    "El código que generes será ejecutado automáticamente y el resultado se mostrará al usuario. "
    "Si no es necesario código, responde normalmente. "
    "Si te preguntan por un término técnico, da una definición concisa y precisa."
)

def query_groq_api(question, context=None, memory=None, summary=None):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    history_msgs = []
    if summary:
        history_msgs.append({"role": "system", "content": f"Resumen de la conversación hasta ahora: {summary}"})
    if memory:
        for m in memory:
            if m["role"] == "user":
                history_msgs.append({"role": "user", "content": m["content"]})
            elif m["role"] == "bot":
                history_msgs.append({"role": "assistant", "content": m["content"]})
    if context:
        user_prompt = f"Usa la siguiente información para responder de forma breve pero completa y clara. Si te preguntan por un término técnico, da una definición concisa y precisa.\n\nContexto:\n{context}\n\nPregunta: {question}"
    else:
        user_prompt = question
    history_msgs.append({"role": "user", "content": user_prompt})
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            *history_msgs
        ],
        "max_tokens": 80,
        "temperature": 0.7
    }
    response = requests.post(GROQ_API_URL, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"] 