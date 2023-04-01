# app/patch.py
"""
HTTP PATCH requests are to make a partial update on a resource. To make it more precise – the PATCH method is the
correct choice for partially updating an existing resource. You should only use PUT if you’re replacing a resource in
its entirety.

Support for PATCH in browsers, servers, and web application frameworks is not universal. Lots of software have
missing or broken support for it.

The PATCH method is not a replacement for the POST or PUT methods. It applies a delta (diff) rather than replacing
the entire resource.

The difference between the PUT and PATCH APIs are that PUT is a full update as PATCH is a partial update.

If an existing resource is modified, either the 200 (OK) or 204 (No Content) response codes SHOULD be sent to indicate
successful completion of the request.
"""
from fastapi import APIRouter, HTTPException, status
from app.definitions import IDPrice, IDQuantity
from app.redis_db import redis
from app.definitions import REDIS_HOSTNAME, REDIS_PORT
from redis import exceptions
from app.logs import logger

router = APIRouter()

@router.patch("/api/item/id/price", status_code=status.HTTP_200_OK, tags=["patch"])
def updatePrice(update_price: IDPrice) -> dict:
    """
    This API updated the price of an item given its ID.

    A request body is data sent by the client to your API in the message body. To declare one in FastAPI,
    we can use Pydantic models. PUT requests pass their data in the message body. The data parameter takes
    JSON format identical to Python dictionary. The 'keys' need to be identical to the Pydantic models.

    if the resource does not exist, this API returns a 404 not found.

    If the client makes a typo or sends a wrong key/value pair, the server will send a:
        HTTP/1.1 422 Unprocessable Entity

    curl -X PATCH -H "Content-type: application/json" -H "Accept: application/json" \
    -d '{"item_id":100, "price": 99.99}' -i -L "http://localhost:8000/api/item/id/price"
    :param update_price: class IDPrice(BaseModel)
    :return: The updated item
    """
    # Hash HEXISTS
    key = 'item:' + str(update_price.item_id)
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

    if not result:
        strError = f"Item with ID {update_price.item_id} doesn't exists, price update failed"
        logger.info(f'{strError}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strError,
            headers={"X-Fake-REST-API": strError},
        )

    try:
        result = redis.hset(key, 'price', update_price.price)
    except exceptions.ConnectionError:
        strError = f"Connection error: Redis database {REDIS_HOSTNAME}:{REDIS_PORT}"
        logger.info(f'{strError}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=strError,
            headers={"X-Fake-REST-API": strError},
        )

    if result == 0:
        return {"detail": "update successful", "Item": update_price.item_id, "New Price": update_price.price}

    # This should never happen
    strError = f"ERROR: Field price was added for ID {update_price.item_id}"
    logger.info(f'{strError}')
    raise HTTPException(
        status_code=status.HTTP_201_CREATED,
        detail=strError,
        headers={"X-Fake-REST-API": strError},
    )

@router.patch("/api/item/id/quantity", status_code=status.HTTP_200_OK, tags=["patch"])
def updateQuantity(update_quantity: IDQuantity) -> dict:
    """
    This API updated the quantity of an item given its ID.

    A request body is data sent by the client to your API in the message body. To declare one in FastAPI,
    we can use Pydantic models. PUT requests pass their data in the message body. The data parameter takes
    JSON format identical to Python dictionary. The 'keys' need to be identical to the Pydantic models.

    if the resource does not exist, this API returns a 404 not found.

    If the client makes a typo or sends a wrong key/value pair, the server will send a:
        HTTP/1.1 422 Unprocessable Entity

    curl -X PATCH -H "Content-type: application/json" -H "Accept: application/json" \
    -d '{"item_id":100, "quantity": 0}' -i -L "http://localhost:8000/api/item/id/quantity"
    :param update_quantity: class IDPrice(BaseModel)
    :return: The updated item
    """
    # Hash SET
    key = 'item:' + str(update_quantity.item_id)
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

    if not result:
        strError = f"Item with ID {update_quantity.item_id} doesn't exists, quantity update failed"
        logger.info(f'{strError}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strError,
            headers={"X-Fake-REST-API": strError},
        )

    try:
        result = redis.hset(key, 'quantity', update_quantity.quantity)
    except exceptions.ConnectionError:
        strError = f"Connection error: Redis database {REDIS_HOSTNAME}:{REDIS_PORT}"
        logger.info(f'{strError}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=strError,
            headers={"X-Fake-REST-API": strError},
        )

    if result == 0:
        return {"detail": "update successful", "Item": update_quantity.item_id, "New Price": update_quantity.quantity}

    # This should never happen
    strError = f"ERROR: Field price was added for ID {update_quantity.item_id}"
    logger.info(f'{strError}')
    raise HTTPException(
        status_code=status.HTTP_201_CREATED,
        detail=strError,
        headers={"X-Fake-REST-API": strError},
    )


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
