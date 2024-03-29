# app/post.py
"""
Use POST APIs to create new resources. When talking strictly about REST, POST methods are used to create a
new resource into the collection of resources. Responses to this method are not cacheable unless the response
includes appropriate Cache-Control or Expires header fields. POST is neither safe nor idempotent. you can't use
this method more than once and expect a consistent outcome or result.

Ideally, if a resource has been created on the origin server, the response SHOULD be HTTP response code 201 (Created).
Many times, the action performed by the POST method might not result in a resource that can be identified by a URI.
In this case, either HTTP response code 200 (OK) or 204 (No Content) is the appropriate response status.
"""
from fastapi import APIRouter, HTTPException, status
from app.definitions import Item
from app.redis_db import redis
from app.definitions import REDIS_HOSTNAME, REDIS_PORT
from fastapi.encoders import jsonable_encoder
from redis import exceptions
from app.logs import logger

router = APIRouter()

@router.post("/api/item", status_code=status.HTTP_201_CREATED, tags=["post"])
def add_item(item: Item) -> dict:
    """
    A request body is data sent by the client to your API in the message body. To declare one in FastAPI,
    we can use Pydantic models. POST requests pass their data in the message body. The data parameter takes
    JSON format identical to Python dictionary. The 'keys' need to be identical to the Pydantic models.

    If the client makes a typo or sends a wrong key/value pair, the server will send a:
        HTTP/1.1 422 Unprocessable Entity

    curl -X POST -H "Content-type: application/json" -H "Accept: application/json" \
    -d '{"id":100,"description":"This is a description","price": 99.99,"quantity": 100,"category": "clothes"}' \
    -i -L "http://localhost:8000/api/item"
    :param item:
    :return: The data received in the body
    """
    # Hash GET
    key = 'item:' + str(item.id)
    try:
        result = redis.hget(key, 'id')
    except exceptions.ConnectionError:
        strError = f"Connection error: Redis database {REDIS_HOSTNAME}:{REDIS_PORT}"
        logger.info(f'{strError}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=strError,
            headers={"X-Fake-REST-API": strError},
        )
    if result:
        strError = f"ID {item.id} already exists, adding item failed"
        logger.info(f'{strError}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=strError,
            headers={"X-Fake-REST-API": strError},
        )
    # Hash Multiple Set
    redis.hset(key, mapping=jsonable_encoder(item))
    logger.info(f'POST: {item}')
    return dict(item)


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
