# main.py
import uvicorn
import logging
import platform

if __name__ == "__main__":
    # logger config
    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s: %(levelname)s %(funcName)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.info(f'Python version: {platform.python_version()}')
    logging.info(f'Hostname: {platform.node()}')
    
    HOSTNAME = "0.0.0.0"
    PORT = 8000

    # Method GET
    uvicorn.run("app.get:app", host=HOSTNAME, port=PORT, log_level="info")

    # Method POST
    # uvicorn.run("app.post:app", host=HOSTNAME, port=PORT, log_level="info")

    # Method PUT
    # uvicorn.run("app.put:app", host=HOSTNAME, port=PORT, log_level="info")

    # Method PATCH
    # uvicorn.run("app.patch:app", host=HOSTNAME, port=PORT, log_level="info")

    # Method HEAD
    # uvicorn.run("app.head:app", host=HOSTNAME, port=PORT, log_level="info")

    # Method TRACE
    # uvicorn.run("app.trace:app", host=HOSTNAME, port=PORT, log_level="info")

    # Method OPTIONS
    # uvicorn.run("app.options:app", host=HOSTNAME, port=PORT, log_level="info")

    # Method DELETE
    # uvicorn.run("app.delete:app", host=HOSTNAME, port=PORT, log_level="info")
