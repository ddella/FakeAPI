# app/head.py
from fastapi import APIRouter, Request
import app.database as db

router = APIRouter()

@router.head("/", tags=["head"])
async def head(request: Request) -> dict:
    """
    The HTTP HEAD method requests HTTP headers from the server as if the document was requested using
    the HTTP GET method. The only difference between HTTP HEAD and GET requests is that for HTTP HEAD,
    the server only returns headers without body. The "content-length" field reflects the total amount
    of data that would have been returned by the server.

    curl -I -H "Content-type: application/json" -H "Accept: application/json" -i -L "http://localhost:8000"
    :return: Only the header of a query
    """
    items = db.readData()
    return {"message": "Root of Fake REST API", "method": request.method, "items": items}

if __name__ == "__main__":
    import uvicorn
    import logging
    import platform
    from fastapi import FastAPI
    from definitions import tags_metadata, HOSTNAME, PORT

    # logger config
    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s: %(levelname)s %(funcName)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.info(f'Python version: {platform.python_version()}')
    logging.info(f'Hostname: {platform.node()}')

    app = FastAPI(openapi_tags=tags_metadata)
    app.include_router(router)

    uvicorn.run(app, host=HOSTNAME, port=PORT, log_level="info")
