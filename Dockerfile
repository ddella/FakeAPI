# Use the following command to build the Docker image:
#   docker build -t fakeapi:2.0 .
# (Optional) If you suspect somethings wrong, you can start the container with the command:
#   docker run -it --rm --name fakeapi fakeapi:2.0 /bin/sh
#
FROM python:3.11-alpine3.17

# set the working directory for the app
RUN ["mkdir", "-p", "/usr/src/app"]
WORKDIR /usr/src/app

# copy the scripts to the folder
COPY src/ .

# install dependencies
RUN ["pip3", "install", "fastapi", "uvicorn", "pydantic", "pydantic[email]", "passlib", "PyJWT", "redis"]
# RUN ["pip3", "install", "-r", "requirements.txt"]

# start the FakeAPI server
CMD [ "python3", "./main.py" ]