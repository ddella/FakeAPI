# app/options.py
from fastapi import APIRouter, status, Response

router = APIRouter()

@router.options("/{full_path:path}", status_code=status.HTTP_204_NO_CONTENT, tags=["options"])
async def options(response: Response, full_path: str):
    """
    The OPTIONS method is designed to communicate to the client which of the methods are available to them
    on a given item or collection. If a path is specified, a filed is added in the header of the response.
    Example with curl:
        curl -X OPTIONS -H "Content-type: application/json" -H "Accept: application/json" \
        -i -L "http://localhost:8000/"
    :return: The header with the method(s) supported by the server
    """
    headers = {"Allow": "OPTIONS, GET, POST, PUT, DELETE, TRACE, PATCH",
               "Cache-Control": "max-age=604800"}
    if full_path:
        headers.update({"X-Fake-API-path-error": full_path})
    response.status_code = status.HTTP_204_NO_CONTENT
    response.headers.update(headers)
    return

if __name__ == "__main__":
    import uvicorn
    import logging
    import platform
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
