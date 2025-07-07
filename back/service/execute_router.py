from fastapi import APIRouter, Request
import sys
import io

execute_router = APIRouter()

def run_python_code(code: str) -> str:
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = mystdout = io.StringIO()
    sys.stderr = mystderr = io.StringIO()
    safe_globals = {"__builtins__": {"print": print, "range": range, "len": len, "sum": sum, "min": min, "max": max, "abs": abs}}
    safe_locals = {}
    try:
        exec(code, safe_globals, safe_locals)
        output = mystdout.getvalue() + mystderr.getvalue()
        if not output:
            output = "<No output>"
        return output
    except Exception as e:
        return f"Error: {repr(e)}"
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

@execute_router.post("/execute")
async def execute_code(request: Request):
    data = await request.json()
    code = data.get("code", "")
    if not code:
        return {"result": "No code provided."}
    output = run_python_code(code)
    return {"result": output} 