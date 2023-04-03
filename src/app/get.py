# app/get.py
"""
Use GET requests to retrieve resource representation/information only – and not modify it in any way.
As GET requests do not change the resource’s state, these are said to be safe methods.
Additionally, GET APIs should be idempotent. Making multiple identical requests must produce the same result
every time until another API (POST or PUT) has changed the state of the resource on the server.
If the Request-URI refers to a data-producing process, it is the produced data that shall be returned as the entity
in the response and not the source text of the process, unless that text happens to be the output of the process.

Type of parameter(s) passed with the API:
    1. No parameter(s)
    2. Path parameter(s)
    3. Query parameter(s)
    4. Content body parameter(s)
"""

from fastapi import APIRouter, status, HTTPException
from fastapi.responses import RedirectResponse
from redis import exceptions
from app.redis_db import redis
from app.definitions import IDPrice, REDIS_HOSTNAME, REDIS_PORT
from app.logs import logger

router = APIRouter()

def get_id_price(item_id, price) -> dict:
    # Hash GETALL
    key = 'item:' + str(item_id)
    try:
        result = redis.hgetall(key)
    except exceptions.ConnectionError:
        strError = f"Connection error: Redis database {REDIS_HOSTNAME}:{REDIS_PORT}"
        logger.info(f'{strError}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=strError,
            headers={"X-Fake-REST-API": strError},
        )

    if not result:
        strError = f"Item with ID {item_id} was not found"
        logger.info(f'{strError}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strError,
            headers={"X-Fake-REST-API": strError},
        )

    if int(result.get('id')) == item_id and float(result.get('price')) == price:
        return {"Item": result}
    else:
        strError = f"Item with ID {item_id} and price {price:.2f}$ was not found"
        logger.info(f'{strError}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strError,
            headers={"X-Fake-REST-API": strError},
        )

def get_id(item_id: int) -> dict:
    # Hash GETALL
    key = 'item:' + str(item_id)
    try:
        result = redis.hgetall(key)
    except exceptions.ConnectionError:
        strError = f"Connection error: Redis database {REDIS_HOSTNAME}:{REDIS_PORT}"
        logger.info(f'{strError}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=strError,
            headers={"X-Fake-REST-API": strError},
        )

    if not result:
        strError = f"Item with ID {item_id} was not found"
        logger.info(f'{strError}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strError,
            headers={"X-Fake-REST-API": strError},
        )

    return {"Item": result}

@router.get("/", response_class=RedirectResponse, include_in_schema=False)
async def docs():
    """
    This router redirects to the swagger page at location: /docs
    :return:
    """
    return RedirectResponse(url='/docs')

# @router.get("/", status_code=status.HTTP_308_PERMANENT_REDIRECT, tags=["root"])
# async def root(response: Response) -> None:
#     """
#     This router redirects to the swagger page at location: /docs
#     :param response:
#     :return:
#     """
#     headers = {"Location": "/docs"}
#     response.headers.update(headers)
#     return

@router.get("/api/item/{item_id}", tags=["path_parameter"])
def path_parameter_id(item_id: int):
    """
    The value of the path parameter 'item_id' will be passed to the function path_parameter()
    as the argument 'item_id'. The name of the path parameter MUST be identical to the function argument.

    Example with curl:
        curl -H "Content-type: application/json" \
        -H "Accept: application/json" -i -L "http://127.0.0.1:8000/api/item/{item_id}"
    :param item_id: The ID of the resource we want to retreive
    :return:
    """
    return get_id(item_id)

@router.get("/api/item/price/{item_id}/{price}", tags=["path_parameter"])
def path_parameter_id_price(item_id: int, price: float):
    """
    Path parameters help scope the API call down to a single resource, which means you don’t have to build a body for
    something as simple as a resource finder.
    These parameters are enclosed in curly brackets {}, and they offer a way for you to control the representation of
    specific resources. They’re placed before the query string and within the path of an endpoint.

    The value of the path parameter 'item_id' will be passed to the function path_parameter()
    as the argument 'item_id'. The name of the path parameter MUST be identical to the function argument.

    Example with curl:
        curl -H "Content-type: application/json" \
        -H "Accept: application/json" -i -L "http://127.0.0.1:8000/api/item/price/{item_id}/{price}"
    :param item_id: The ID of the resource we want to retreive
    :param price: The price of the resource we want to retreive
    :return:
    """
    return get_id_price(item_id, price)

@router.get("/api/item/0/price", tags=["query_parameter"])
def query_parameter(item_id: int, price: float):
    """
    Query parameters are optional. In FastAPI, function parameters that aren’t declared as part of the path parameters
    are automatically interpreted as query parameters.

    The query is the set of key-value pairs that comes after the question mark '?' in a URL,
    separated by an ampersand '&'.

    Example of 2 'Query parameters' URL's:
    The 1st URL has a trailing '/' after item. The consequence is that you'll get an HTTP/1.1 307 Temporary Redirect
    http://127.0.0.1:8000/api/item/0/price/?price=1.99&str_item_id=100

    The 2nd URL doens't have a trailing '/' after item, and you get an HTTP/1.1 200 OK without any redirect.
    http://127.0.0.1:8000/api/item/0/price?price=1.99&str_item_id=100

    The query parameters are:
    'price' with a value of '1.99' and 'str_item_id' with a value of '100'.

    The value of the query parameter 'price' and 'str_item_id' will be passed to the function query_parameter()
    as the argument 'price' and 'str_item_id'. The name of the path parameter MUST be identical to the function
    argument.

    Example with curl:
        curl -H "Content-type: application/json" \
        -H "Accept: application/json" -i -L "http://127.0.0.1:8000/api/item/0/price?price=1.99&item_id=100"
    :param price:
    :param item_id:
    :return:
    """
    return get_id_price(item_id, price)

@router.get("/api/item/1/price", status_code=status.HTTP_200_OK, tags=["content_parameter"])
async def content_parameter(itemPrice: IDPrice):
    """
    In a request body, data sent by the client to your API in the body of the request. To declare one in FastAPI,
    we can use Pydantic models. In this example we want to find a resource with a specific ID and price.

    Example with curl:
        curl -X GET -H "Content-type: application/json" -H "Accept: application/json" \
        -d '{"item_id": 123, "price": 9.99}' -i -L "http://localhost:8000/api/item/1/price"
    :param itemPrice: Item ID and price of item we want to retreive
    :return: The item or error 404 if not found
    """
    return get_id_price(itemPrice.item_id, itemPrice.price)

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
