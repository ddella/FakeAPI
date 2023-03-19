# app/trace.py
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
import platform
from .definitions import *

app = FastAPI(openapi_tags=tags_metadata)

@app.trace("/{full_path:path}", status_code=status.HTTP_200_OK, tags=["trace"])
async def trace(request: Request, full_path: str):
    """
    The TRACE method is for diagnosis purposes. It creates a loop-back test with the same request header that
    the client sent to the server. The TRACE method is safe, idempotent and returns successful response code 200 OK.
    Example with curl:
        curl -X TRACE -H "Content-type: application/json" -H "Accept: application/json" -H "trace: trace-method-test"\
        -i -L "http://localhost:8000/"
    :return: The header sent by the client in the content
    """
    clientHeader = dict(request.headers.items())
    headers = {"X-Fake-API-trace": "client header returned"}
    content = {"header": clientHeader, "hostname": platform.node()}
    if full_path:
        content.update({"X-Fake-API-path-error": full_path})
    return JSONResponse(content=content, headers=headers)
