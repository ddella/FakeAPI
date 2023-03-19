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
from fastapi import FastAPI, HTTPException, status
from .definitions import *

app = FastAPI(openapi_tags=tags_metadata)

@app.post("/api/item", status_code=status.HTTP_201_CREATED, tags=["post"])
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
    print(items)
    record = [d for d in items if d.id == item.id]
    if record:
        # record is a list with only one element, if ID is unique 😉
        strError = f"ID {item.id} already exists, adding item failed"
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=strError,
            headers={"X-Fake-REST-API": strError},
        )
    items.append(item)
    return dict(item)
