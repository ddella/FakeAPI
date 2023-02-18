from fastapi import FastAPI, Response, status, Request, HTTPException
from fastapi.responses import JSONResponse  # , HTMLResponse
from logger import logging
import platform
import uvicorn
import os
from config import settings
from database import MongoDB
from pydantic import BaseModel
from enum import Enum

app = FastAPI(docs_url="/docs", redoc_url=None)

class Item(BaseModel):
    id: str
    description: str
    price: float
    quantity: int

class FilterID(BaseModel):
    id: str

class Price(BaseModel):
    id: str
    price: float

class Quantity(BaseModel):
    id: str
    quantity: int

class Description(BaseModel):
    id: str
    description: str

# The URLs for the 'patchItem' function
class PatchURL(str, Enum):
    price = "price"
    quantity = "quantity"
    description = "description"

@app.patch('/api/patch/item/{patchURL}', status_code=status.HTTP_200_OK)
async def patchItem(patchURL: PatchURL, item: dict):
    """
    This is the main entry point for URI: /api/patch/item/{patchURL}
    This function calls the corresponding function based on the URI
    :param patchURL: Check the class 'PatchURL' for possible values
    :param item: The new value to modify
    :return:
    """
    # URL = /api/patch/item/price
    if patchURL is patchURL.price:
        price = Price.parse_obj(item)  # map dict to Pydantic Model
        # Partial update of an object, if it doesn't exist then throw an error
        logging.info(f'patchURL Price={patchURL} - NewPrice={price.price}')
        val = patchItemPrice(price)
        return val

    # URL = /api/patch/item/quantity
    if patchURL is patchURL.quantity:
        quantity = Quantity.parse_obj(item)  # map dict to Pydantic Model
        # Partial update of an object, if it doesn't exist then throw an error
        logging.info(f'patchURL Quantity={patchURL} - NewQuantity={quantity.quantity}')
        val = patchItemQuantity(quantity)
        return val

    # URL = /api/patch/item/description
    if patchURL is patchURL.description:
        description = Description.parse_obj(item)  # map dict to Pydantic Model
        # Partial update of an object, if it doesn't exist then throw an error
        logging.info(f'patchURL Description={patchURL} - NewDescription={description.description}')
        val = patchItemDescription(description)
        return val

def patchItemPrice(price: Price):
    """
    Use PATCH APIs to make a partial update on a ressource.
    If ressource doesn't exist, throw an error.
    URI: https://localhost:8443/patchItem/price/
    Example with curl:
        curl -X PATCH -H "Content-type: application/json" \
        -H "Accept: application/json" \
        -d '{"id":"123456789", "price": 666.66}' \
        -i -L "https://localhost:9443/api/patch/item/price"
    :return:
    """
    # Partial update of an object, if it doesn't exist then throw an error
    record = db.findOneDocument({'id': price.id})
    if record:
        # Object already exists, update it
        db.updateOne({'id': price.id}, {'price': price.price})
        logging.info(f'Object {price} updated')
        return {'success': 'data updated', 'partial': price}
    else:
        # Object not in database, throw an error
        strError = f'Object {price.id} not in database'
        logging.info(strError)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strError,
            headers={"X-Fake-REST-API": strError},
        )

def patchItemQuantity(quantity: Quantity):
    """
    Use PATCH APIs to make a partial update on a ressource.
    If ressource doesn't exist, throw an error.
    Example with curl:
        curl -X PATCH -H "Content-type: application/json" \
        -H "Accept: application/json" \
        -d '{"id":"123456789", "quantity": 37}' \
        -i -L "https://localhost:9443/api/patch/item/quantity"
    :return:
    """
    # Partial update of an object, if it doesn't exist then throw an error
    record = db.findOneDocument({'id': quantity.id})
    if record:
        # Object already exists, throw an error
        db.updateOne({'id': quantity.id}, {'quantity': quantity.quantity})
        logging.info(f'Object {quantity} updated')
        return {'success': 'data updated', 'partial': quantity}
    else:
        # Object not in database, throw an error
        strError = f'Object {quantity.id} not in database'
        logging.info(strError)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strError,
            headers={"X-Fake-REST-API": strError},
        )

def patchItemDescription(description: Description):
    """
    Use PATCH APIs to make a partial update on a ressource.
    If ressource doesn't exist, throw an error.
    Example with curl:
        curl -X PATCH -H "Content-type: application/json" \
        -H "Accept: application/json" \
        -d '{"id":"000000001", "description": "This is a new and updated description"}' \
        -i -L "https://localhost:9443/api/patch/item/description"
    :return:
    """
    # Partial update of an object, if it doesn't exist then throw an error
    record = db.findOneDocument({'id': description.id})
    if record:
        # Object already exists, update it
        db.updateOne({'id': description.id}, {'description': description.description})
        logging.info(f'Object {description} updated')
        return {'success': 'data updated', 'partial': description}
    else:
        # Object not in database, throw an error
        strError = f'Object {description.id} not in database'
        logging.info(strError)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strError,
            headers={"X-Fake-REST-API": strError},
        )

@app.delete('/api/delete/item/id', status_code=status.HTTP_200_OK)
async def deleteOneItem(item: FilterID):
    """
    Use DELETE APIs to delete a resource.
    Example with curl:
        curl -X DELETE -H "Content-type: application/json" \
        -H "Accept: application/json" \
        -d '{"id":"850703190"}' \
        -i -L "https://localhost:9443/api/delete/item/id"
    :return:
    """
    # DELETE an object, if it exists
    record = db.findOneDocument({'id': item.id})
    if record:
        # Object exists, delete it
        db.delOneDocument({'id': item.id})
        logging.info(f'Object {item} deleted')
        return {'success': 'data deleted', 'object': item}
    else:
        # Object not in database, throw an error
        strError = f'Object {item.id} not found'
        logging.info(strError)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strError,
            headers={"X-Fake-REST-API": strError},
        )

@app.put('/api/update/item', status_code=status.HTTP_200_OK)
async def updateOneItem(item: Item, response: Response):
    """
    Use PUT APIs to make a full update on a resource. If the resource does not exist,
    then API may decide to create a new resource or not. In this examaple we do create the resource.
    Example with curl:
        curl -X PUT -H "Content-type: application/json" \
        -H "Accept: application/json" \
        -d '{"id":"000000001","description":"Resistors", "price": 0.99, "quantity": 101}' \
        -i -L "https://localhost:9443/api/update/item"
    :param response: 200 for updated item or 201 for creating item
    :param item: A dictionnary with the new item
    :return:
    """
    record = db.addOneDocument({'id': item.id}, dict(item))
    if record:
        # Object already exists, update successful
        logging.info(f'Object {item} updated successfully')
        return {'success': 'data updated', 'object': item}
    else:
        # Object not in database, so add it
        logging.info(f'Object {item} added successfully')
        response.status_code = status.HTTP_201_CREATED
        return {'success': 'data added', 'object': item}

@app.post('/api/add/item', status_code=status.HTTP_201_CREATED)
async def addOneItem(item: Item):
    """
    Use POST APIs to create one object, if the object exists it throws an error
    URI: http://localhost/api/add/item
    Example with curl:
        curl -X POST -H "Content-type: application/json" \
        -H "Accept: application/json" \
        -d '{"id":"123456789","description":"Resistors", "price": 0.99, "quantity": 100}' \
        -i -L "https://localhost:9443/api/add/item"
    :param item: The new object
    :return: status code and new object, if creation successful
    """
    # db.addOneDocument({'id': item.id}, dict(item))
    # return {'success': 'data added', 'newobject': item}
    record = db.findOneDocument({'id': item.id})
    if record:
        # Object already exists, throw an error
        strError = f'Object {item.id} exists, use PUT or PATCH'
        logging.info(strError)
        raise HTTPException(
            status_code=409,
            detail=strError,
            headers={"X-Fake-REST-API": strError},
        )
    else:
        # Object not in database, so add it
        db.addOneDocument({'id': item.id}, dict(item))
        logging.info(f'Object {item} added at {platform.node()}')
        return {'success': 'data added', 'newobject': item}
#
@app.api_route("/api/allitem", methods=['GET', 'HEAD'])
async def allItem(response: Response, request: Request):
    """
    Returns all the items from the database. This code could return lots of object.
    Not for production!
    Returns 200 for GET and 204 for HEAD.
    Example with curl (add '-I' for HEAD method):
        curl -H "Content-type: application/json" \
        -H "Accept: application/json" \
        --insecure -i -L "https://localhost:9443/api/allitem"
    :return: HTTP_200_OK or HTTP_204_NO_CONTENT
    """
    item = db.getTotalDocument()
    headers = {"X-FakeAPI-EndPoint": request.url.path, "X-FakeAPI-Method": request.method,
               "X-FakeAPI-Items": str(item)}
    if request.method == 'GET':
        content = db.viewAllDocuments()
        response.status_code = status.HTTP_200_OK
        return JSONResponse(content=content, headers=headers)
    if request.method == 'HEAD':
        response.status_code = status.HTTP_204_NO_CONTENT
        response.headers.update(headers)
        return

@app.api_route("/api/totalitem", methods=['GET', 'HEAD'])
async def totalItem(response: Response, request: Request):
    """
    Returns the total number of items in the database. Doesn't return the items.
    Returns 200 for GET and 204 for HEAD. You could add more code for specific test
    Example with curl (add '-I' for HEAD method):
        curl -H "Content-type: application/json" \
        -H "Accept: application/json" \
        --insecure -i -L "https://localhost:9443/api/totalitem"
    :return: HTTP_200_OK or HTTP_204_NO_CONTENT
    """
    logging.info(f'Inside "totalitem" end point')
    headers = {"X-FakeAPI-EndPoint": request.url.path, "X-FakeAPI-Method": request.method}
    if request.method == 'GET':
        item = db.getTotalDocument()
        content = {"items": item}
        response.status_code = status.HTTP_200_OK
        return JSONResponse(content=content, headers=headers)
    if request.method == 'HEAD':
        response.status_code = status.HTTP_204_NO_CONTENT
        response.headers.update(headers)
        return

@app.api_route("/api/healthcheck", methods=['GET', 'HEAD'])
async def healthcheck(response: Response, request: Request):
    """
    Returns 200 for GET and 204 for HEAD. You could add more code for specific test
    As an example, you could test a database connectivity
    Return health status of the API
    Example with curl (add '-I' for HEAD method):
        curl -H "Content-type: application/json" \
        -H "Accept: application/json" \
        --insecure -i -L "https://localhost:9443/api/healthcheck"
    :return: HTTP_200_OK or HTTP_204_NO_CONTENT
    """
    if request.method == 'GET':
        content = {"Health": "OK", "PID": os.getpid(), "hostname": platform.node()}
        headers = {"X-Fake-API": "/api/healthcheck", "X-Method": "Method was GET"}
        response.status_code = status.HTTP_200_OK
        # return {"message": "Welcome to FakeAPI with MongoDB"}
        return JSONResponse(content=content, headers=headers)
    if request.method == 'HEAD':
        headers = {"X-Fake-API": "/api/healthcheck", "X-Method": "Method was HEAD"}
        response.status_code = status.HTTP_204_NO_CONTENT
        response.headers.update(headers)
        return

@app.trace("/{full_path:path}", status_code=status.HTTP_200_OK)
async def trace(request: Request, full_path: str):
    """
    The TRACE method is for diagnosis purposes. It creates a loop-back test with the same request header that
    the client sent to the server. The TRACE method is safe, idempotent and returns successful response code 200 OK.
    Example with curl:
        curl -X TRACE -H "Content-type: application/json" \
        -H "Accept: application/json" -H "trace: trace-method-test"\
        -i -L "https://localhost:9443/"
    :return: The header sent by the client
    """
    clientHeader = dict(request.headers.items())
    headers = {"X-Fake-API-trace": "client header returned"}
    content = {"header": clientHeader, "hostname": platform.node()}
    if full_path:
        content.update({"path-error": full_path})
    return JSONResponse(content=content, headers=headers)

@app.options("/{full_path:path}", status_code=status.HTTP_204_NO_CONTENT)
async def options(response: Response):
    """
    The OPTIONS method is designed to communicate to the client which of the methods
    are available to them on a given item or collection.
    Example with curl:
        curl -X OPTIONS -H "Content-type: application/json" \
        -H "Accept: application/json" \
        --insecure -i -L "https://localhost:9443/"
    :return: The header with the methods supported by the server
    """
    headers = {"Allow": "OPTIONS, GET, POST, PUT, DELETE, TRACE, PATCH"}
    response.status_code = status.HTTP_204_NO_CONTENT
    response.headers.update(headers)
    return

@app.api_route("/{path_name:path}", methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS'],
               status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
async def catch_all(request: Request, path_name: str):
    """
    Catch all 'route'. Returns error 405
    Example with curl (add '-I' for HEAD method):
        curl -H "Content-type: application/json" \
        -H "Accept: application/json" \
        --insecure -i -L "https://localhost:9443/api/bad_endpoint"
    :return: HTTP_405_METHOD_NOT_ALLOWED
    """
    logging.info(f'catch all method: "method": {request.method}, "endpoint": {path_name}')
    return {"status": "Error catch all", "method": request.method, "endpoint": path_name}


if __name__ == "__main__":
    # Prints the Python version
    logging.info(f'Python version: {platform.python_version()}')
    logging.info(f'Hostname: {platform.node()}')

    # Get the listening interface
    try:
        HOST = settings.FAKEAPI_HOST
    except KeyError:
        logging.debug(f'Missing host configuration for REST API, using default "0.0.0.0"')
        HOST = "0.0.0.0"

    # Get the listening TCP port
    try:
        PORT = settings.FAKEAPI_PORT
    except KeyError:
        logging.debug(f'Missing TCP PORT configuration for REST API, using default "TCP/443"')
        PORT = 443

    # Get the private key & certificate. If either one is missimg, revert to HTTP
    try:
        SERVER_KEY = settings.FAKEAPI_PKEY
        logging.debug(f'Read Private Key from file "{SERVER_KEY}"')
    except KeyError:
        logging.debug(f"Missing private key configuration for REST API, using default HTTP")
        SERVER_CRT = None
        SERVER_KEY = None
    else:
        # Get the certificate
        try:
            SERVER_CRT = settings.FAKEAPI_CRT
            logging.debug(f'Read X.509 Certificate from file "{SERVER_CRT}"')
        except KeyError:
            logging.debug(f"Missing X.509 certificate configuration for REST API, using default HTTP")
            SERVER_CRT = None
            SERVER_KEY = None

    # Init the database
    db = MongoDB()
    if db.myDatabase is None:
        logging.error(f'Quitting apps, database error')
        exit(255)

    # Start the server
    uvicorn.run(app, host=HOST, port=PORT,
                ssl_keyfile=SERVER_KEY,
                ssl_certfile=SERVER_CRT,
                # ssl_ca_certs="ca-chain.pem",
                # ssl_ciphers="TLSv1.2",
                # log_level="info")
                # log requests from client
                # access_log=True,
                log_level="info")
    del db
