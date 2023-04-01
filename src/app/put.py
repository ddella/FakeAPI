# app/put.py
"""
Use PUT APIs primarily to do a FULL update an existing resource (if the resource does not exist, then API may decide
to create a new resource or not). If the request passes through a cache and the Request-URI identifies one or more
currently cached entities, those entries SHOULD be treated as stale. Responses to PUT method are not cacheable.

The difference between the POST and PUT APIs can be observed in request URIs. POST requests are made on resource
collections, whereas PUT requests are made on a single resource.

HTTP POST http://localhost/api/item
HTTP PUT http://localhost/api/item/id

If a new resource has been created by the PUT API, the origin server MUST inform the user agent via the HTTP response
code 201 (Created) response.
If an existing resource is modified, either the 200 (OK) or 204 (No Content) response codes SHOULD be sent to indicate
successful completion of the request.
"""
from fastapi import APIRouter, HTTPException, status
from app.definitions import Item
from app.redis_db import redis
from app.definitions import REDIS_HOSTNAME, REDIS_PORT
from fastapi.encoders import jsonable_encoder
from redis import exceptions
from app.logs import logger

router = APIRouter()

@router.put("/api/item/id", status_code=status.HTTP_200_OK, tags=["put"])
def update_item(updated_item: Item) -> dict:
    """
    A request body is data sent by the client to your API in the message body. To declare one in FastAPI,
    we can use Pydantic models. PUT requests pass their data in the message body. The data parameter takes
    JSON format identical to Python dictionary. The 'keys' need to be identical to the Pydantic models.

    if the resource does not exist, this API decides NOT to create a new resource.

    If the client makes a typo or sends a wrong key/value pair, the server will send a:
        HTTP/1.1 422 Unprocessable Entity

    curl -X PUT -H "Content-type: application/json" -H "Accept: application/json" \
    -d '{"id":100,"description":"This is a description","price": 99.99,"quantity": 100,"category": "clothes"}' \
    -i -L "http://localhost:8000/api/item/id"
    :param updated_item: class Item(BaseModel):
    :return: The updated item
    """
    # Hash HEXISTS
    key = 'item:' + str(updated_item.id)
    try:
        result = redis.hexists(key, 'id')
    except exceptions.ConnectionError:
        strError = f"Connection error: Redis database {REDIS_HOSTNAME}:{REDIS_PORT}"
        logger.info(f'{strError}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=strError,
            headers={"X-Fake-REST-API": strError},
        )

    if result:
        # Hash Multiple Set
        redis.hset(key, mapping=jsonable_encoder(updated_item))
        logger.info(f'Full update - {jsonable_encoder(updated_item)}')
        return dict(updated_item)

    strError = f"Item with ID {updated_item.id} doesn't exists, full update failed"
    logger.info(f'{strError}')
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=strError,
        headers={"X-Fake-REST-API": strError},
    )


if __name__ == "__main__":
    import uvicorn
    import logging
    import platform
    from fastapi import FastAPI
    from definitions import HOSTNAME, PORT, tags_metadata

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
