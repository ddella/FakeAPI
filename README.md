<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>

# What is FakeAPI

FakeAPI is a Python script that implements most of the REST API methods. Do not use it in a production deployment. The script does almost no testing to keep the code small. I build it to learn more about the concept of REST API and also to test some API Gateways, like [MuleSoft](https://www.mulesoft.com/).

>Implements only `JSON` objects. Sorry no `XML` 😉

The script requires the following Python modules:
* pydantic
* uvicorn
* fastapi

REST API methods implemented in FakeAPI:
* **HTTP GET** to retrieve information
* **HTTP POST** to create a new resource
* **HTTP PUT** to Update/Replace a resource
* **HTTP DELETE** to delete a resource
* **HTTP PATCH** to make a Partial Update/Modify

# How to use this image
## This is for educationnal **only**!

## Build the image with the Dockerfile in your Python app project
This is my `Dockerfile`:

    FROM python:alpine

    RUN ["mkdir", "-p", "/usr/src/data"]
    WORKDIR /usr/src/app

    COPY ["requirements.txt", "./"]
    RUN ["pip", "install", "--no-cache-dir", "-r", "requirements.txt"]

    COPY ["./FakeREST_API.py", "./"]

    EXPOSE 8000

    CMD [ "python", "./FakeREST_API.py" ]

After the build, the imaage should be `~78Mb`.

```sh
docker build -t fakeapi .
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Run the project with the data file inside the container.
The data will be lost when the container exits.
```sh
docker run -it --rm -p 8000:8000 --name fakeapi --hostname fakeapi1 fakeapi
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Run the project with the data file on the Docker host.
Mount the container `/usr/src/data` directory on the current directory of the host. Data will be on the Docker host when the container exits. The container also run in interactive mode because of the `-it` switch. This way you can look at the logs.
```sh
docker run -it --rm -v $PWD:/usr/src/data -p 8000:8000 --name fakeapi --hostname fakeapi1 fakeapi
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Shell access
Get shell access to the container with the `/usr/src/data` directory mounted on the current directory of the host.
```sh
docker run -it --rm --hostname fakeapi1 -v $PWD:/usr/src/data fakeapi /bin/sh
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

If the object was found, it returns HTTP status code 409:

    HTTP/1.1 409 Conflict
    date: Sun, 01 Jan 2023 00:00:00 GMT
    server: uvicorn
    x-fake-rest-api: Object 123456789 exists at localhost.local, use PUT or PATCH
    content-length: 75
    content-type: application/json

    {"detail":"Object 123456789 exists at localhost.local, use PUT or PATCH"}

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License
Distributed under the MIT License. See `LICENSE.txt` for more information.
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

