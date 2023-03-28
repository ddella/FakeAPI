# app/trace.py
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
import platform

router = APIRouter()

@router.trace("/{full_path:path}", status_code=status.HTTP_200_OK, tags=["trace"])
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


if __name__ == "__main__":
    import uvicorn
    import logging
    from definitions import tags_metadata, HOSTNAME, PORT
    from fastapi import FastAPI

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
