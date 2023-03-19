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
from fastapi import FastAPI, HTTPException, status
from .definitions import *

app = FastAPI(openapi_tags=tags_metadata)

@app.put("/api/item/id", status_code=status.HTTP_200_OK, tags=["put"])
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
    idx_item_to_update = [i for i, x in enumerate(items) if x.id == updated_item.id]
    if idx_item_to_update:
        items.pop(idx_item_to_update[0])
        items.insert(idx_item_to_update[0], updated_item)
        return dict(updated_item)

    strError = f"Item with ID {updated_item.id} doesn't exists, full update failed"
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=strError,
        headers={"X-Fake-REST-API": strError},
    )
