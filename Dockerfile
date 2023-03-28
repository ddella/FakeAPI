# Use the following command to build the Docker image:
#   docker build -t fakeapi .
# (Optional) If you suspect somethings wrong, you can start the container with the command:
#   docker run -it --rm --name fakeapi fakeapi /bin/sh
#
FROM python:alpine

# create the database directory
RUN ["mkdir", "-p", "/usr/src/data"]

# set the working directory for the app
RUN ["mkdir", "-p", "/usr/src/app"]
WORKDIR /usr/src/app

# install dependencies
RUN ["pip", "install", "fastapi", "uvicorn", "pydantic", "pydantic[email]", "passlib", "PyJWT", "redis"]

# copy the scripts to the folder
COPY src/ .

# start the server
CMD [ "python", "./main.py" ]