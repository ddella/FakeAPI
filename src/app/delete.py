# app/delete.py
from fastapi import FastAPI, status, HTTPException
from .definitions import *

app = FastAPI(openapi_tags=tags_metadata)

@app.delete('/api/delete/id/', status_code=status.HTTP_200_OK, tags=["delete"])
async def deleteItem(item_id: ItemID) -> dict:
    """
    Use DELETE method to delete a specified resource by ID. If it doesn't exist, return 404. The parameter is of type
    "ItemID" because we need to pass it in the content of the request. It's not a path or query parameter.

    Example with curl:
        curl -X DELETE -H "Content-type: application/json" -H "Accept: application/json" \
        -d '{"item_id": 123}' -i -L "http://localhost:8000/api/delete/id/"
    :param item_id: ID of item to delete
    :return: Deleted item or error 404 if not found
    """
    idx_item_to_remove = [i for i, x in enumerate(items) if x.id == item_id.item_id]
    if idx_item_to_remove:
        bad_item = items.pop(idx_item_to_remove[0])
        return dict(bad_item)

    strError = f"Item with ID {item_id.item_id} doesn't exists, delete failed"
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=strError,
        headers={"X-Fake-REST-API": strError},
    )
