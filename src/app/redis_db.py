# app/redis_db.py
"""
Example with a simple GET against a Redis database.
You can start a Redis Docker container with the command:
    docker run --name redis.lab --hostname redis.lab -it --rm --network backend -p 6379:6379 redis --loglevel notice

Start a Redis client for troubleshooting. Note that the hostname is 'redis.lab' because we're in the same network
as the server. Don't use 'localhost':
    docker run -it --rm --network backend redis redis-cli -h redis.lab
Example of queries with the Redis client:
    HGETALL item:100

If this script is run on the host, the Redis server is at 'localhost'
If this script is run in a container, the Redis server is at 'redis.lab'
"""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import HTMLResponse
from redis import Redis, exceptions
import time
import platform
from app.definitions import REDIS_HOSTNAME, REDIS_PORT
from app.logs import logger

# Get the id of the docker container we're running in (it's our hostname)
container_id = platform.node()

# Connect to redis and create a key for number of time visited, if it didn't exist
try:
    redis = Redis(host=REDIS_HOSTNAME, port=REDIS_PORT, db=0, socket_connect_timeout=5,
                  socket_timeout=5, decode_responses=True, charset='utf-8')
    # redis.set(container_id, 0)
    visited_key = 'visited:' + container_id
    try:
        setnx_result = redis.setnx(visited_key, 0)
    except Exception as e:
        logger.error(f'Error: {e}')
    else:
        if setnx_result:
            logger.info(f'Key: "{visited_key}" created')
        else:
            logger.info(f'Key: "{visited_key}" already exist')
except Exception as e:
    logger.error(f'Connection failed with Redis database {REDIS_HOSTNAME} at port {REDIS_PORT}')
else:
    logger.info(f'Connected to Redis database {REDIS_HOSTNAME}:{REDIS_PORT}')

router = APIRouter()

def get_hit_count():
    retries = 3
    while True:
        try:
            return redis.incr(container_id)
        except exceptions.ConnectionError:
            if retries == 0:
                return -1
            retries -= 1
            time.sleep(0.5)

def generate_html_response(num_visited: int):
    html_content = f"""
    <html>
        <head>
            <title>Redis Example</title>
        </head>
        <body>
            <h2>You visited me {num_visited}</h2>
            <h2>Container ID is {container_id}</h2>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@router.get("/redis", response_class=HTMLResponse)
async def my_redis():
    # Increment the number of requests
    count = get_hit_count()
    if count < 0:
        strError = f'Problem with Redis database {REDIS_HOSTNAME} at port {REDIS_PORT}'
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=strError,
            headers={"X-Fake-REST-API": strError},
        )
    return generate_html_response(count)


if __name__ == "__main__":
    import uvicorn
    import logging
    import platform
    from fastapi import FastAPI
    from definitions import tags_metadata, HOSTNAME, PORT, Item
    from fastapi.encoders import jsonable_encoder

    @router.post("/api/item", status_code=status.HTTP_201_CREATED, tags=["post"])
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
        # Hash GET
        key = 'item:' + str(item.id)
        try:
            result = redis.hget(key, 'id')
        except exceptions.ConnectionError:
            strError = f"Connection error: Redis database {REDIS_HOSTNAME}:{REDIS_PORT}"
            logger.info(f'{strError}')
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=strError,
                headers={"X-Fake-REST-API": strError},
            )

        logging.info(f'HGET: {result} - Key={key}')

        if result:
            strError = f"ID {item.id} already exists, adding item failed"
            logger.info(f'{strError}')
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=strError,
                headers={"X-Fake-REST-API": strError},
            )
        # Hash Multiple Set
        result = redis.hset(key, mapping=jsonable_encoder(item))
        logging.info(f'HSET: {result} - {jsonable_encoder(item)}')
        return dict(item)

    # logger config
    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s: %(levelname)s %(funcName)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.info(f'Python version: {platform.python_version()}')
    logging.info(f'Hostname: {platform.node()}')
    logging.info(f'Redis database module')

    app = FastAPI(openapi_tags=tags_metadata)
    app.include_router(router)

    uvicorn.run(app, host=HOSTNAME, port=PORT, log_level="info")
