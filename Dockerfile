# Build
# docker build -t fakeapi .
FROM python:alpine

RUN ["mkdir", "-p", "/usr/src/data"]
WORKDIR /usr/src/app

COPY ["./src/requirements.txt", "./"]
RUN ["pip", "install", "--no-cache-dir", "-r", "requirements.txt"]

COPY ["./src/*", "./"]

CMD [ "python", "./app.py" ]
