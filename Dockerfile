# Build
# docker build -t fakeapi .
FROM python:alpine

RUN ["mkdir", "-p", "/usr/src/data"]
WORKDIR /usr/src/app

COPY ["requirements.txt", "./"]
RUN ["pip", "install", "--no-cache-dir", "-r", "requirements.txt"]

COPY ["./FakeREST_API.py", "./"]

EXPOSE 8000

CMD [ "python", "./FakeREST_API.py" ]
