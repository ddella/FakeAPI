# main.py
import uvicorn
import logging
import platform
from fastapi import FastAPI
from app.definitions import tags_metadata, HOSTNAME, PORT

import app.delete as delete     # DELETE method
import app.get as get           # GET method
import app.head as head         # HEAD method
import app.options as options   # OPTIONS method
import app.patch as patch       # PATCH method
import app.post as post         # POST method
import app.put as put           # PUT method
import app.trace as trace       # TRACE method

if __name__ == "__main__":
    # logger config
    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s: %(levelname)s %(funcName)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.info(f'Python version: {platform.python_version()}')
    logging.info(f'Hostname: {platform.node()} listening on interface {HOSTNAME}:{PORT}')

    app = FastAPI(openapi_tags=tags_metadata)
    app.include_router(delete.router)
    app.include_router(get.router)
    app.include_router(head.router)
    app.include_router(options.router)
    app.include_router(patch.router)
    app.include_router(post.router)
    app.include_router(put.router)
    app.include_router(trace.router)

    uvicorn.run(app, host=HOSTNAME, port=PORT, log_level="info")
