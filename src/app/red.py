# app/secret.py
"""
Example with a simple GET against a Redis database.
You can start a Redis Docker container with the command:
    docker run --name redis --hostname redis -d --rm --network backend -p 6379:6379 redis

If this script is run on the host, the Redis server is at 'localhost'
If this script is run in a container, the Redis server is at 'redis'
"""

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from redis import Redis, exceptions
import time
import platform

# Get the id of the docker container we're running in (it's our hostname)
container_id = platform.node()

# Connect to redis and set num_requests to 0 if it doesn't exist
try:
    redis = Redis(host='redis', port=6379)
    # redis.set(container_id, 0)
    redis.setnx(container_id, 0)
except exceptions.ConnectionError:
    print('error Redis')

router = APIRouter()

def get_hit_count():
    retries = 3
    while True:
        try:
            return redis.incr(container_id)
        except exceptions.ConnectionError:
            if retries == 0:
                return 0
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
    return generate_html_response(count)


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
