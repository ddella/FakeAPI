# app/delete.py
# https://fastapi.tiangolo.com/it/tutorial/bigger-applications/
from fastapi import status, HTTPException, APIRouter
from app.definitions import ItemID
from app.redis_db import redis
from app.definitions import REDIS_HOSTNAME, REDIS_PORT
from redis import exceptions
from app.logs import logger

router = APIRouter()

@router.delete('/api/delete/id/', status_code=status.HTTP_200_OK, tags=["delete"])
async def deleteItem(item_id: ItemID) -> dict:
    """
    Use DELETE method to delete a specified resource by ID. If it doesn't exist, return 404.
    The parameter is of type "ItemID" because we need to pass it in the content of the request.
    It's not a path or query parameter.

    Example with curl:
        curl -X DELETE -H "Content-type: application/json" -H "Accept: application/json" \
        -d '{"item_id": 123}' -i -L "http://localhost:8000/api/delete/id/"
    :param item_id: ID of item to delete
    :return: Deleted item or error 404 if not found
    """
    key = 'item:' + str(item_id.item_id)
    try:
        result = redis.delete(key)
    except exceptions.ConnectionError:
        strError = f"Connection error: Redis database {REDIS_HOSTNAME}:{REDIS_PORT}"
        logger.info(f'{strError}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=strError,
            headers={"X-Fake-REST-API": strError},
        )

    if result == 1:
        logger.info(f'delete successful for item {item_id.item_id}')
        return {"detail": "delete successful", "Item": item_id.item_id}

    strError = f"Item with ID {item_id.item_id} doesn't exists, delete failed"
    logger.info(f'{strError}')
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
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
