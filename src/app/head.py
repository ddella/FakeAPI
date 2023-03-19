# app/head.py
from fastapi import FastAPI, Request
from .definitions import *

app = FastAPI(openapi_tags=tags_metadata)

@app.head("/", tags=["head"])
async def head(request: Request) -> dict:
    """
    The HTTP HEAD method requests HTTP headers from the server as if the document was requested using
    the HTTP GET method. The only difference between HTTP HEAD and GET requests is that for HTTP HEAD,
    the server only returns headers without body. The "content-length" field reflects the total amount
    of data that would have been returned by the server.

    curl -I -H "Content-type: application/json" -H "Accept: application/json" -i -L "http://localhost:8000"
    :return: Only the header of a query
    """
    return {"message": "Root of Fake REST API", "method": request.method, "items": items}
