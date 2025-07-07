from fastapi import APIRouter, Request
from service.rag import search_context, init_rag
from service.model import query_groq_api
from service.memoria import (
    conversation_memory, conversation_summary, MAX_TOKENS_HISTORY,
    init_memoria, count_tokens, summarize_history
)
from langchain_core.messages import HumanMessage, AIMessage
from service.execute_router import run_python_code
import re
import os
import base64

chat_router = APIRouter()

@chat_router.on_event("startup")
def startup_event():
    init_rag()
    init_memoria()

def extract_python_code(text):
    match = re.search(r"```python\s*([\s\S]+?)```", text)
    if match:
        return match.group(1).strip()
    return None

def image_to_base64(image_path):
    if not image_path or not os.path.exists(image_path):
        print(f"[IMG][ERROR] No existe la imagen: {image_path}")
        return None
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    except Exception as e:
        print(f"[IMG][ERROR] Error convirtiendo a base64: {e}")
        return None

def find_image_by_filename(filename):
    images_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images')
    for f in os.listdir(images_dir):
        if filename in f:
            return os.path.join(images_dir, f)
    return None

@chat_router.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()
    question = data.get('question', '')
    if not question:
        return {"response": "No question provided.", "rag_used": False}
    conversation_memory.save_context({"input": question}, {"output": ""})
    tokens = count_tokens()
    history = "\n".join([
        f"Usuario: {m.content}" if isinstance(m, HumanMessage) else f"Bot: {m.content}"
        for m in conversation_memory.buffer if m.content.strip()
    ])
    summary = None
    if tokens > MAX_TOKENS_HISTORY:
        summary = summarize_history(history)
        conversation_memory.clear()
        conversation_memory.save_context({"input": f"[RESUMEN] {summary}"}, {"output": ""})
    match = re.search(r"([\w\-]+\.pdf_p\d+_\d+)", question)
    if match:
        filename = match.group(1)
        image_path = find_image_by_filename(filename)
        if image_path:
            image_b64 = image_to_base64(image_path)
            response = {
                "response": f"He encontrado la imagen '{filename}' en el PDF y te la muestro a continuación:",
                "image_base64": image_b64,
                "rag_used": False
            }
            return response
    rag_result = search_context(question)
    context = rag_result["context"]
    image_path = rag_result["image_path"]
    rag_used = bool(context)
    image_b64 = None
    if image_path:
        image_b64 = image_to_base64(image_path)
    try:
        memory_msgs = []
        for m in conversation_memory.buffer:
            if isinstance(m, HumanMessage):
                memory_msgs.append({"role": "user", "content": m.content})
            elif isinstance(m, AIMessage):
                memory_msgs.append({"role": "bot", "content": m.content})
        answer = query_groq_api(question, context, memory_msgs, summary)
        code = extract_python_code(answer)
        exec_result = None
        if code:
            exec_result = run_python_code(code)
        conversation_memory.save_context({"input": ""}, {"output": answer})
        response_payload = {"response": answer, "rag_used": rag_used}
        if exec_result is not None:
            response_payload["response"] += f"\n\n[Resultado de la ejecución Python]:\n{exec_result}"
        if image_b64:
            response_payload["image_base64"] = image_b64
        return response_payload
    except Exception as e:
        print(f"[BACKEND][ERROR] {repr(e)}")
        return {"response": f"Error en backend: {repr(e)}", "rag_used": rag_used} 