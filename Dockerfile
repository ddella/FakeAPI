# Build
# docker build -t fakeapi .
FROM python:alpine

# set the working directory
RUN ["mkdir", "-p", "/usr/src/data"]
WORKDIR /usr/src/app

# install dependencies
COPY ["./src/requirements.txt", "./"]
RUN ["pip", "install", "--no-cache-dir", "-r", "requirements.txt"]

# copy the scripts to the folder
COPY ["./src/*", "./"]

# start the server
CMD [ "python", "./app.py" ]
