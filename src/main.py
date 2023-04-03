# main.py
"""
Start a Redis server in a custom network. We need Docker's DNS for name resolution
    % docker run --name redis.lab --hostname redis.lab -it --rm --network backend -p 6379:6379 redis --loglevel notice

Start a Redis client for troubleshooting. Note that the hostname is 'redis.lab' because we're in the same network
as the server. Don't use 'localhost' as this container is in the same network as the Redis server and Docker's
DNS will take care of resolution:
    % docker run -it --rm --network backend redis redis-cli -h redis.lab

Example of queries within the Redis client:
    redis.lab:6379> HGETALL item:100
"""
import uvicorn
import logging
import platform
from fastapi import FastAPI
from app.definitions import tags_metadata, HOSTNAME, PORT, SERVER_CRT, SERVER_KEY

import app.delete as delete     # DELETE method
import app.get as get           # GET method
import app.head as head         # HEAD method
import app.options as options   # OPTIONS method
import app.patch as patch       # PATCH method
import app.post as post         # POST method
import app.put as put           # PUT method
import app.trace as trace       # TRACE method
import jwtauth.users as users   # module for users
import app.redis_db as redis    # GET method with Redis database

if __name__ == "__main__":
    # logger config
    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s: %(asctime)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.info(f'Hostname: {platform.node()} listening on interface {HOSTNAME}:{PORT}')

    if not SERVER_KEY:
        logging.info(f'HTTP activated')
    else:
        logging.info(f'HTTPS activated with Server Certificate={SERVER_CRT} - Server Private Key={SERVER_KEY}')

    app = FastAPI(openapi_tags=tags_metadata)
    app.include_router(delete.router)
    app.include_router(get.router)
    app.include_router(head.router)
    app.include_router(options.router)
    app.include_router(patch.router)
    app.include_router(post.router)
    app.include_router(put.router)
    app.include_router(trace.router)

    # JWT auth modules
    app.include_router(users.router)

    # Redis example
    app.include_router(redis.router)

    # Start the server
    uvicorn.run(app, host=HOSTNAME, port=PORT,
                ssl_keyfile=SERVER_KEY,
                ssl_certfile=SERVER_CRT,
                # ssl_ca_certs="ca-chain.pem",
                # ssl_ciphers="TLSv1.2",
                access_log=True,
                log_level="info")
