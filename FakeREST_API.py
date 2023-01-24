"""
This is a tutorial script to show the basics of REST API. It implements most of the methods.
Do not use it in a production deployment. The script does almost no testing. This is on purpose
to keep the code "light".

Doesn't implement XML, returns JSON objects only.
This script implements fake REST API with the following HTTP methods:
    HTTP GET->      retrieve information
    HTTP POST->     create new resource
    HTTP PUT->      Update/Replace
    HTTP DELETE->   delete a resource
    HTTP PATCH->    Partial Update/Modify

Example of file 'data.json':
[{"id": "111111111", "description": "This is a description", "price": 1.11, "quantity": 111},
 {"id": "222222222", "description": "This is another description", "price": 2.22, "quantity": 222}
]

Credits:
Official documentation
https://fastapi.tiangolo.com/
https://realpython.com/fastapi-python-web-apis/#learn-more-about-fastapi

REST API status code
https://restfulapi.net/http-status-codes/
REST API method
https://restfulapi.net/http-methods/
"""
from fastapi import FastAPI, HTTPException, Response, status, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging
import json
import os
import uvicorn
import platform
from enum import Enum

class Item(BaseModel):
    id: str
    description: str
    price: float
    quantity: int

# The URLs for the 'patchItem' function
class PatchURL(str, Enum):
    price = "price"
    quantity = "quantity"
    description = "description"


# Simulation of our database
importedSyntheticData = list()
# The file that has the full data for this example
data = 'data.json'
# data = '/usr/src/data/data.json'
# Swagger UI to be served at /docs and disable ReDoc:
app = FastAPI(docs_url="/docs", redoc_url=None)

@app.api_route("/", methods=['GET', 'HEAD'], status_code=status.HTTP_200_OK)
async def root(response: Response, request: Request):
    """
    This is the root of the Fake REST API.
    Example with curl (add '-I' for HEAD method):
        curl -H "Content-type: application/json" \
        -H "Accept: application/json" \
        -i -L "http://localhost:8000/"
    :return: A message and the hostname of the server
    """
    logging.debug(f'request.method={request.method} - {type(request.method)}')
    headers = {"uri": "FakeREST API root"}
    # response.status_code = status.HTTP_204_NO_CONTENT
    response.headers.update(headers)
    return {"message": "Root of Fake REST API", "hostname": platform.node()}

@app.api_route("/healthcheck", methods=['GET', 'HEAD'])
async def healthcheck(response: Response, request: Request):
    """
    Returns 200 for GET and 204 for HEAD. You could add more code for specific test
    As an example, you could test a database connectivity
    Return health status of the API
    Example with curl (add '-I' for HEAD method):
        curl -H "Content-type: application/json" \
        -H "Accept: application/json" \
        -i -L "http://localhost:8000/healthcheck"
    :return: HTTP_200_OK or HTTP_204_NO_CONTENT
    """
    if request.method == 'GET':
        content = {"Health": "OK", "PID": os.getpid(), "hostname": platform.node()}
        headers = {"X-Fake-API": "/healthcheck", "X-Method": "Method was GET"}
        response.status_code = status.HTTP_200_OK
        return JSONResponse(content=content, headers=headers)
    if request.method == 'HEAD':
        headers = {"X-Fake-API": "/healthcheck", "X-Method": "Method was HEAD"}
        response.status_code = status.HTTP_204_NO_CONTENT
        response.headers.update(headers)
        return

@app.api_route("/errorCode/{code}", methods=['GET', 'HEAD'])
async def errorCode(code: int):
    """
    Return the error code in the HTTP header
    URI: http://localhost/errorCode/{code}
    Example with curl (add '-I' for HEAD method):
        curl -H "Content-type: application/json" \
        -H "Accept: application/json" \
        -i -L "http://localhost:8000/errorCode/404"
    :return:
    """
    logging.info(f'Code = {code} from {platform.node()}')
    strError = f"Error code {code} from {platform.node()}"
    raise HTTPException(
        status_code=code,
        detail=strError,
        headers={"X-Fake-REST-API": strError},
    )

# @app.head("/id/{identification}", status_code=200)
# @app.get("/id/{identification}", status_code=200)
@app.api_route("/id/{identification}", methods=['GET', 'HEAD'], status_code=status.HTTP_200_OK)
async def getItem(identification: str):
    """
    Query the database for a specific object
    URI: http://localhost/id/{identification}
    GET method (add '-I' for HEAD method):
    Example with curl:
      curl -H "Content-type: application/json" \
      -H "Accept: application/json" \
      -i -L "http://localhost:8000/id/562641783"
    :return: {"id":"xx","description":"A description","price":15.67,"quantity":32}
    """
    record = [d for d in importedSyntheticData if d.get('id') == identification]
    if record:
        logging.info(f'Found ID {identification} from {platform.node()}')
        return record
    else:
        logging.info(f'ID {identification} was NOT found from {platform.node()}')
        strError = f"ID {identification} not found"
        raise HTTPException(
            status_code=404,
            detail=strError,
            headers={"X-Fake-REST-API": strError},
        )

@app.post('/addItem/', status_code=status.HTTP_201_CREATED)
async def addItem(item: Item):
    """
    Use POST APIs to create new object, if the object exists it throws an error
    URI: http://localhost/addItem/
    Example with curl:
        curl -X POST -H "Content-type: application/json" \
        -H "Accept: application/json" \
        -d '{"id":"123456789","description":"This is a description", "price": 99.99, "quantity": 100}' \
        -i -L "http://localhost:8000/addItem/"
    :param item: The new object
    :return: status code and new object, if creation successful
    """
    record = [aDict for aDict in importedSyntheticData if item.id in aDict.values()]
    if record:
        # Object already exists, throw an error
        logging.info(f'Object {item.id} exists at {platform.node()}, use PUT or PATCH')
        strError = f'Object {item.id} exists at {platform.node()}, use PUT or PATCH'
        raise HTTPException(
            status_code=409,
            detail=strError,
            headers={"X-Fake-REST-API": strError},
        )
    else:
        # Object not in dictionnary, so add it
        newDict = item.dict()
        importedSyntheticData.append(newDict)
        # write data to file
        writeJSON(data, importedSyntheticData)
        logging.info(f'Object {item} added at {platform.node()}')
        return {'success': 'data added', 'newobject': newDict}

@app.put('/updateItem/', status_code=status.HTTP_200_OK)
async def update_item(item: Item, response: Response):
    """
    Use PUT APIs to make a full update on a resource. If the resource does not exist,
    then API may decide to create a new resource or not. In this examaple we do create the resource.
    URI: http://localhost:8000/updateItem/
    Example with curl:
        curl -X PUT -H "Content-type: application/json" \
        -H "Accept: application/json" \
        -d '{"id":"123456789","description":"This is a description", "price": 99.99, "quantity": 100}' \
        -i -L "http://localhost:8000/updateItem/"
    :param response: 200 for updated item or 201 for creating item
    :param item: A dictionnary with the new item
    :return:
    """
    newDict = item.dict()
    # record = [aDict for aDict in importedSyntheticData if item.id in aDict.values()]
    index = [i for i, aDict in enumerate(importedSyntheticData) if item.id in aDict.values()]
    if index:
        # Object was found, we apply a full update on it
        importedSyntheticData[index[0]] = item.dict()
        logging.info(f'Update successful for item {item} at {platform.node()}')
        # write data to file
        writeJSON(data, importedSyntheticData)
        return {'success': 'data updated', 'newobject': newDict}
    else:
        # Object was not found, so add it
        importedSyntheticData.append(newDict)
        # write data to file
        writeJSON(data, importedSyntheticData)
        logging.info(f'Added item {item} at {platform.node()}')
        # Return status 201: created
        response.status_code = status.HTTP_201_CREATED
        return {'success': 'data added', 'newobject': newDict}

@app.delete('/deleteItem/id/', status_code=status.HTTP_200_OK)
async def deleteItem(item: dict):
    """
    Use DELETE APIs to delete a resource.
    URI: http://localhost:8000/deleteItem/
    Example with curl:
        curl -X DELETE -H "Content-type: application/json" \
        -H "Accept: application/json" \
        -d '{"id":"123456789"}' \
        -i -L "http://localhost:8000/deleteItem/id/"
    :return:
    """
    # DELETE an object, if it doesn't exist then throw an error
    index = [i for i, aDict in enumerate(importedSyntheticData) if item.get("id") in aDict.values()]
    if index:
        record = importedSyntheticData.pop(index[0])
        logging.info(f'Delete successful for item {record} at {platform.node()}')
        # write data to file
        writeJSON(data, importedSyntheticData)
        strSuccess = f'Delete of item "{item.get("id")}" successful at {platform.node()}'
        return {'success': strSuccess, 'item': record}
    else:
        logging.info(f'Object wasn\'t found on {platform.node()}')
        strError = f'Item {item} was not found'
        raise HTTPException(
            status_code=404,
            detail=strError,
            headers={"X-Fake-REST-API": strError},
        )

@app.patch('/patchItem/{patchURL}/', status_code=status.HTTP_200_OK)
async def patchItem(patchURL: PatchURL, item: dict):
    """
    This is the main entry point for URI: /patchItem/{patchURL}
    This function calls the corresponding function based on the URI
    :param patchURL: Check the class 'PatchURL' for possible valaues
    :param item: The new value to modify
    :return:
    """
    # URL = /patchItem/price/
    if patchURL is patchURL.price:
        # Partial update of an object, if it doesn't exist then throw an error
        val = patchItemPrice(item)
        return val

    # URL = /patchItem/quantity/
    if patchURL is patchURL.quantity:
        # Partial update of an object, if it doesn't exist then throw an error
        val = patchItemQuantity(item)
        return val

    # URL = /patchItem/description/
    if patchURL is patchURL.description:
        # Partial update of an object, if it doesn't exist then throw an error
        val = patchItemDescription(item)
        return val

@app.trace("/{full_path:path}", status_code=status.HTTP_200_OK)
async def trace(request: Request, full_path: str):
    """
    The TRACE method is for diagnosis purposes. It creates a loop-back test with the same request header that
    the client sent to the server. The TRACE method is safe, idempotent and returns successful response code 200 OK.
    Example with curl:
        curl -X TRACE -H "Content-type: application/json" \
        -H "Accept: application/json" -H "trace: trace-method-test"\
        -i -L "http://localhost:8000/"
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
        -i -L "http://localhost:8000/"
    :return: The header with the methods supported by the server
    """
    headers = {"Allow": "OPTIONS, GET, POST, PUT, DELETE, TRACE, PATCH"}
    response.status_code = status.HTTP_204_NO_CONTENT
    response.headers.update(headers)
    return

def patchItemPrice(item: dict):
    """
    Use PATCH APIs to make a partial update on a ressource.
    If ressource doesn't exist, throw an error.
    URI: http://localhost:8000/patchItem/price/
    Example with curl:
        curl -X PATCH -H "Content-type: application/json" \
        -H "Accept: application/json" \
        -d '{"id":"123456789", "newprice": 666.66}' \
        -i -L "http://localhost:8000/patchItem/price/"
    :return:
    """
    # Partial update of an object, if it doesn't exist then throw an error
    index = [i for i, aDict in enumerate(importedSyntheticData) if aDict.get("id") == item.get('id')]
    if index:
        # Update element of an object from the start (index = 0)
        importedSyntheticData[index[0]]['price'] = item.get('newprice')
        strSuccess = f'Update of "price" successful for item {importedSyntheticData[index[0]]} on'
        strSuccess += f' {platform.node()}'
        logging.info(strSuccess)
        # write data to file
        writeJSON(data, importedSyntheticData)
        return {'success': 'Update of price successful', 'item': importedSyntheticData[index[0]]}
    else:
        logging.info(f'Object was not found on {platform.node()} in patchItemPrice')
        strError = f'Object was not found on {platform.node()} in patchItemPrice'
        raise HTTPException(
            status_code=404,
            detail=strError,
            headers={"X-Fake-REST-API": strError},
        )

def patchItemQuantity(item: dict):
    """
    Use PATCH APIs to make a partial update on a ressource.
    If ressource doesn't exist, throw an error.
    URI: http://localhost:8000/patchItem/quantity/
    Example with curl:
        curl -X PATCH -H "Content-type: application/json" \
        -H "Accept: application/json" \
        -d '{"id":"123456789", "newquantity": 666}' \
        -i -L "http://localhost:8000/patchItem/quantity/"
    :return:
    """
    # Partial update of an object, if it doesn't exist then throw an error
    index = [i for i, aDict in enumerate(importedSyntheticData) if aDict.get("id") == item.get('id')]
    if index:
        # Update element of an object from the start (index = 0)
        importedSyntheticData[index[0]]['quantity'] = item.get('newquantity')
        strSuccess = f'Update of "quantity" successful for item {importedSyntheticData[index[0]]}.'
        strSuccess += f'Hostname: {platform.node()}'
        logging.info(strSuccess)
        # write data to file
        writeJSON(data, importedSyntheticData)
        return {'success': 'Update of quantity successful', 'item': importedSyntheticData[index[0]]}
    else:
        logging.info(f'Object was not found on {platform.node()} in patchItemQuantity')
        strError = f'Object was not found on {platform.node()} in patchItemQuantity'
        raise HTTPException(
            status_code=404,
            detail=strError,
            headers={"X-Fake-REST-API": strError},
        )

def patchItemDescription(item: dict):
    """
    Use PATCH APIs to make a partial update on a ressource.
    If ressource doesn't exist, throw an error.
    URI: http://localhost:8000/patchItem/description/
    Example with curl:
        curl -X PATCH -H "Content-type: application/json" \
        -H "Accept: application/json" \
        -d '{"id":"123456789", "newdescription": "This is a new description"}' \
        -i -L "http://localhost:8000/patchItem/description/"
    :return:
    """
    # Partial update of an object, if it doesn't exist then throw an error
    index = [i for i, aDict in enumerate(importedSyntheticData) if aDict.get("id") == item.get('id')]
    if index:
        # Update element of an object from the start (index = 0)
        importedSyntheticData[index[0]]['description'] = item.get('newdescription')
        strSuccess = f'Update of "description" successful for item {importedSyntheticData[index[0]]}.'
        strSuccess += f'Hostname: {platform.node()}'
        logging.info(strSuccess)
        # write data to file
        writeJSON(data, importedSyntheticData)
        return {'success': 'Update of description successful', 'item': importedSyntheticData[index[0]]}
    else:
        logging.info(f'Object was not found on {platform.node()} in patchItemDescription')
        strError = f'Object was not found on {platform.node()} in patchItemDescription'
        raise HTTPException(
            status_code=404,
            detail=strError,
            headers={"X-Fake-REST-API": strError},
        )

def writeJSON(filename, myList):
    """
    Writes the list of dict to the file
    :param filename: name of the file
    :param myList: the list of dict
    :return: True/False
    """
    try:
        out_file = open(filename, 'x', encoding='utf-8')
    except FileExistsError:
        out_file = open(filename, 'w', encoding='utf-8')
        logging.warning(f'Existing file {filename} was overwitten')
    except IOError as e:
        logging.error(f'{e}')
        return False
    json.dump(myList, out_file, indent=3)
    out_file.close()
    return True

def readJSON(filename):
    """
    Read a JSON file that contains a list of dictionnaries that represents synthetic data
    :param filename: JSON file to read
    :return: The data or an empty list
    """
    global importedSyntheticData
    try:
        with open(filename, 'r', encoding='utf-8') as jsonFile:
            data_loaded = json.load(jsonFile)
        jsonFile.close()
        logging.info(f'JSON file "{filename}" was read successfully')
        importedSyntheticData = data_loaded
        return True
    except IOError as e:
        logging.error(f'IOErro: {e}')
        # Empty list of dictionnary
        importedSyntheticData = []
        return False


if __name__ == "__main__":
    # logger config
    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s: %(levelname)s %(funcName)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    # Read the data file (fake database)
    if not readJSON(data):
        writeJSON(data, importedSyntheticData)
        logging.info(f'Empty file {data} created')
    # prints the Python version
    logging.info(f'Python version: {platform.python_version()}')
    logging.info(f'Hostname: {platform.node()}')
    # Start the server
    uvicorn.run(app, host="0.0.0.0", port=8000)
