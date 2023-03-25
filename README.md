<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>

# What is FakeAPI

FakeAPI is a Python script that implements most of the REST API methods. Do not use it in a production deployment. The script does almost no verifications, to keep the code small. I build it to learn more about the concept of REST API and also to test some API Gateways, like [Nginx API Gateway](https://www.nginx.com/learn/api-gateway/) and [MuleSoft](https://www.mulesoft.com/), to name a few.

FakeAPI is based on [FastAPI](https://fastapi.tiangolo.com/) framework. I'm using [Uvicorn](https://www.uvicorn.org/) as the [ASGI](https://asgi.readthedocs.io/en/latest/) web server.

>FakeAPI implements only `JSON` objects. Sorry no `XML` 😉

Take a look at the file `requirement.txt` for the Python modules required:

REST API methods implemented in FakeAPI:
* **HTTP GET** to retrieve information
* **HTTP POST** to create a new resource
* **HTTP PUT** to make a complete Update/Replace
* **HTTP DELETE** to delete a resource
* **HTTP PATCH** to make a partial Update/Modify
* **HTTP TRACE** server reply with the header received

# Python Virtual Environment Setup (Optionnal)
This section is optionnal. Unless you want to play with the source code, you can skip to <a href="#docker-container">How to use this image</a> section.


1. Start by cloning the project and change directory where the source reside:

```sh
gh repo clone ddella/FakeAPI
cd FakeAPI/src
```

2. Create and activate a virtual environment:

```sh
python3.11 -m venv .venv
source .venv/bin/activate
export PYTHONPATH=$PWD
```
>To deactivate the environment, just type `deactivate` in the shell or simply close it.

>Don't forget to export `PYTHONPATH`.

3. Install the necessary modules (make sure you have the latest pip installed):
```sh
pip install --upgrade pip
pip install fastapi uvicorn pydantic
```

4. Create the `requirements.txt` file needed to build the image: 
```sh
pip freeze > requirements.txt
```

5. Make sure you're using the right Python interpreter, the one in the virtual environment:
```sh
(.venv) % which python3
```

The result should be something similar to this (your milage may vary 😀):
```
/Users/username/.../.venv/bin/python3
```
<a name="docker-container"></a>
# How to use this image
## This is for educationnal **only**!
## Build the image with the Dockerfile

This is the `Dockerfile` to build the image:
```Dockerfile
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
RUN ["pip", "install", "fastapi", "uvicorn", "pydantic"]

# copy the scripts to the folder
COPY ["./fakeapi/main.py", "./"]
COPY ["./fakeapi/app/*.py", "./app/"]

# start the server
CMD [ "python", "./main.py" ]
```

```sh
docker build -t fakeapi .
```

>The image should be `~85Mb`.
```sh
docker image ls fakeapi
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

# Run the project
You can run the container with the database outside it. Your data will be retained.

>Use an appropriate `hostname` if you start multiple containers. The logs will print the `hostname`. That will help identify the container. Remember my primary goal is to test API Gateways.

## Run the project with the data file outside the container.
The data will be lost when the container exits.
```sh
docker run -it --rm -v $PWD:/usr/src/data \
-e DATABASE=/usr/src/data/data.json \
--name server1 --hostname server1 --network backend -p8000:8000 \
fakeapi /bin/sh
```
>If you prefer Docker Compose, see [FakeAPI YAML](FakeAPI_YAML.md)

## Custom network (optional)
FakeAPI runs on a custom Docker network. This workshop is not about Docker custom network but I encourage you to run your containers in custom networks to get the added value of a DNS server. The following command was used to create the `backend` network.

```sh
docker network create --driver=bridge --subnet=172.31.11.0/24 --ip-range=172.31.11.128/25 --gateway=172.31.11.1 backend
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Shell access
Get shell access to the container with the `/usr/src/data` directory mounted on the current directory of the host.
```sh
docker run -it --rm --name fakeapi --hostname fakeapi -v $PWD:/usr/src/data fakeapi /bin/sh
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Docs -->
## Docs URLs
You can check the the interactive documentations made available by swagger UI at `http://localhost:8000/docs`.

![Documentation](images/docs.jpg)


<!-- tests -->
# let's get our hands dirty
The best way to test the APIs is with cURL.
<!-- GET Example -->
## Example with GET method
Use this command to query of an object by it's ID:
```shell
curl -H "Content-type: application/json" \
    -H "Accept: application/json" \
    -i -L "http://localhost:8000/id/562641783"
```
This will send a `GET` request to the server. If it finds the object, the server returns the object in `JSON` format like this:

    HTTP/1.1 200 OK
    date: Sun, 01 Jan 2023 00:00:00 GMT
    server: uvicorn
    content-length: 91
    content-type: application/json

    [{"id":"333333333","description":"This is a new description","price":666.66,"quantity":33}]

If the object is not found, it returns HTTP status code 404:

    HTTP/1.1 404 Not Found
    date: Sun, 01 Jan 2023 00:00:00 GMT
    server: uvicorn
    x-fake-rest-api: ID 000000000 not found
    content-length: 35
    content-type: application/json

    {"detail":"ID 000000000 not found"}
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- POST Example -->
## Example with POST method
The `POST` method is used to add a new object. If the new object already exists, it will return an error:

Use this command to add a new object:
```shell
curl -X POST -H "Content-type: application/json" \
    -H "Accept: application/json" \
    -d '{"id":"123456789","description":"This is a description", "price": 99.99, "quantity": 100}' \
    -i -L "http://localhost:8000/addItem/"
```

This will send a `POST` request to the server. If it finds the object, the server returns an error. If it doesn't find the object, it adds it to the database:

    HTTP/1.1 201 Created
    date: Sun, 01 Jan 2023 00:00:00 GMT
    server: uvicorn
    content-length: 122
    content-type: application/json

    {"success":"data added","newobject":{"id":"123456789","description":"This is a description","price":99.99,"quantity":100}}

If the object was not found, it returns HTTP status code 409:

    HTTP/1.1 409 Conflict
    date: Sun, 01 Jan 2023 00:00:00 GMT
    server: uvicorn
    x-fake-rest-api: Object 123456789 exists at localhost.local, use PUT or PATCH
    content-length: 75
    content-type: application/json

    {"detail":"Object 123456789 exists at localhost.local, use PUT or PATCH"}

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- PATCH Example -->
## Example with PATCH method
The `PATCH` method is used for partial update of an existing object:

```shell
curl -X PATCH -H "Content-type: application/json" \
    -H "Accept: application/json" \
    -d '{"id":"123456789", "newprice": 666.66}' \
    -i -L "http://localhost:8000/patchItem/price/"
```

This will send a `PATCH` request to the server. If it finds the object, the server updates only the `price`. If it doesn't find the object, an error is returned:

    HTTP/1.1 200 OK
    date: Sun, 01 Jan 2023 00:00:00 GMT
    server: uvicorn
    content-length: 132
    content-type: application/json

    {"success":"Update of price successful","item":{"id":"123456789","description":"This is a description","price":33.0,"quantity":100}}

If the object was not found, it returns HTTP status code 404:

    HTTP/1.1 404 Not Found
    date: Sun, 01 Jan 2023 00:00:00 GMT
    server: uvicorn
    x-fake-rest-api: Object was not found on localhost.local
    content-length: 54
    content-type: application/json

    {"detail":"Object was not found on localhost.local"}

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- TRACE Example -->
## Example with TRACE method
The `TRACE` method is used for diagnosis purposes. It creates a loop-back test with the same request header that the client sent to the server. The `TRACE` method is safe, idempotent and returns successful response code `200 OK`.

```shell
curl -X TRACE -H "Content-type: application/json" \
    -H "Accept: application/json" -H "trace: trace-method-test"\
    -i -L "http://localhost:8000/"
```

This will send a `TRACE` request to the server and it will reply with the header of received from the client:

    HTTP/1.1 200 OK
    date: Sun, 22 Jan 2023 20:48:50 GMT
    server: uvicorn
    x-fake-api-trace: client header returned
    content-length: 184
    content-type: application/json

    {"header":{"host":"localhost:8000","user-agent":"curl/7.85.0","content-type":"application/json","accept":"application/json","trace":"trace-method-test"},"hostname":"localhost.local"}

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License
Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact
Daniel Della-Noce - [Linkedin](https://www.linkedin.com/in/daniel-della-noce-2176b622/) - daniel@isociel.com

Project Link: [https://github.com/ddella/FakeAPI](https://github.com/ddella/FakeAPI)
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments
* [Official documentation of FastAPI](https://fastapi.tiangolo.com/)
* [Real Python tutorial](https://realpython.com/fastapi-python-web-apis/#learn-more-about-fastapi)
* [REST API status code](https://restfulapi.net/http-status-codes/)
* [REST API method](https://restfulapi.net/http-methods/)
* [Best-README-Template](https://github.com/othneildrew/Best-README-Template/pull/73)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

