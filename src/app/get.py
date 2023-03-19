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

from fastapi import FastAPI, Request, status, HTTPException, Response
from .definitions import *

app = FastAPI(openapi_tags=tags_metadata)

@app.get("/", status_code=status.HTTP_308_PERMANENT_REDIRECT, tags=["root"])
async def root(response: Response) -> None:
    """
    This router redirects to the swagger page at location: /docs
    :param response:
    :return:
    """
    headers = {"Location": "/docs"}
    response.headers.update(headers)
    return

@app.get("/api/items", tags=["get"])
async def get_all_items(request: Request) -> dict:
    """
    Returns all the resources. No parameter needed.

    curl -H "Content-type: application/json" -H "Accept: application/json" -i -L  http://localhost:8000/api/items

    :return: All the elements
    """
    return {"message": "Root of Fake REST API", "method": request.method, "items": items}

@app.get("/api/item/price/{item_id}/{price}", tags=["path_parameter"])
def path_parameter(item_id: int, price: float) -> dict:
    """
    Path parameters help scope the API call down to a single resource, which means you don’t have to build a body for
    something as simple as a resource finder.
    These parameters are enclosed in curly brackets {}, and they offer a way for you to control the representation of
    specific resources. They’re placed before the query string and within the path of an endpoint.

    The value of the path parameter 'item_id' will be passed to the function path_parameter()
    as the argument 'item_id'. The name of the path parameter MUST be identical to the function argument.

    curl -H "Content-type: application/json" \
    -H "Accept: application/json" -i -L "http://127.0.0.1:8000/api/item/price/{item_id}/{price}"
    :param item_id: The ID of the resource we want to retreive
    :param price: The price of the resource we want to retreive
    :return:
    """
    print(f'path_parameter -> ID={item_id} - Price:{price}')
    record = [d for d in items if d.id == item_id]
    if record and record[0].price == price:
        # record is a list with only one element, if ID is unique 😉
        return {"Item": record[0]}
    else:
        strError = f"Item with ID {item_id} and price {price} was not found"
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strError,
            headers={"X-Fake-REST-API": strError},
        )

@app.get("/api/item/0/price", tags=["query_parameter"])
def query_parameter(item_id: int, price: float) -> dict:
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

    curl -H "Content-type: application/json" \
    -H "Accept: application/json" -i -L "http://127.0.0.1:8000/api/item/0/price?price=1.99&item_id=100"
    :param price:
    :param item_id:
    :return:
    """
    print(f'query_parameter -> ID={item_id} - Price:{price}')
    record = [d for d in items if d.id == item_id]
    if record and record[0].price == price:
        # record is a list with only one element, if ID is unique 😉
        return {"Item": record[0]}

    strError = f"Item with ID {item_id} and price {price} was not found"
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=strError,
        headers={"X-Fake-REST-API": strError},
    )

@app.get("/api/item/1/price", status_code=status.HTTP_200_OK, tags=["content_parameter"])
async def content_parameter(itemPrice: IDPrice) -> dict:
    """
    In a request body, data sent by the client to your API in the body of the request. To declare one in FastAPI,
    we can use Pydantic models. In this example we want to find a resource with a specific ID and price.

    Example with curl:
        curl -X GET -H "Content-type: application/json" -H "Accept: application/json" \
        -d '{"item_id": 123, "price": 9.99}' -i -L "http://localhost:8000/api/item/1/price"
    :param itemPrice: Item ID and price of item we want to retreive
    :return: The item or error 404 if not found
    """
    print(f'Content -> ID={itemPrice.item_id} - Price: {itemPrice.price}')
    record = [d for d in items if d.id == itemPrice.item_id]
    if record and record[0].price == itemPrice.price:
        # record is a list with only one element, if ID is unique 😉
        return {"Item": record[0]}

    strError = f"Item with ID {itemPrice.item_id} and price {itemPrice.price} was not found"
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=strError,
        headers={"X-Fake-REST-API": strError},
    )
