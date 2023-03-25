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

# How to use this image (This is for educational **only**!)
## Build the Docker image

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

This command builds the image:

```sh
docker build -t fakeapi .
```

>The image should be `~85Mb`.
```sh
docker image ls fakeapi
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

# Run the project
>**Note**: This project is about REST API and not database. The data is saved in a simple `json` file. The file is mapped outside the container on the Docker host. Multiple container can use the same file but at some point disaster is not too far away 😀 In real life, we should have used a database like [MongoDB](https://www.mongodb.com/).   

Use an appropriate `hostname` if you start multiple containers. The logs will print the `hostname`. That will help identify the container you are hitting, in case you have a load balancer. Remember my primary goal is to test API Gateways/Reverse Proxy and load balancer.

## Run the project with the data file outside the container.
The data will be located on the Docker host in the directory you start the container.

```sh
docker run -d --rm -v $PWD:/usr/src/data \
-e DATABASE=/usr/src/data/data.json \
--name server1 --hostname server1 --network backend -p8000:8000 \
fakeapi
```
>If you prefer Docker Compose, see [FakeAPI YAML](FakeAPI_YAML.md)

## Custom network (optional)
FakeAPI runs on a custom Docker network. This workshop is not about Docker custom network but I encourage you to run your containers in custom networks to get the added value of a DNS server. The following command was used to create the `backend` network.

```sh
docker network create --driver=bridge --subnet=172.31.11.0/24 --ip-range=172.31.11.128/25 --gateway=172.31.11.1 backend
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Shell access
Get shell access to the container with the directory `/usr/src/data`, inside the container,  mounted on the current directory of the Docker host.

```sh
docker run -it --rm --name fakeapi --hostname fakeapi -v $PWD:/usr/src/data fakeapi /bin/sh
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Docs -->
## Docs URLs
You can check the swagger documentation made available at `http://localhost:8000/docs`. This will list all the methods with it's associated endpoints.

![Documentation](images/docs.jpg)


<!-- tests -->
# let's get our hands dirty
The best way to test the APIs is with [cURL](https://curl.se/). Look at the documentation from swagger. A cURL example is included with every function. 

<!-- GET Example -->

## Example with GET method
Use this command to query all the objects in the database:

```shell
curl -H "Content-type: application/json" \
-H "Accept: application/json" \
-i -L "http://localhost:8000/api/items"
```
This will send a `GET` request to the server. If it finds the object, the server returns the object in `JSON` format like this:

    HTTP/1.1 200 OK
    date: Sun, 01 Jan 2023 00:00:00 GMT
    server: uvicorn
    content-length: 613
    content-type: application/json

    {"message":"Root of Fake REST API","method":"GET","items":[{"id":100,"description":"This is a description","price":99.99,"quantity":100,"category":"clothes"},{"id":101,"description":"Jeans","price":39.99,"quantity":100,"category":"clothes"},{"id":102,"description":"Apple","price":0.5,"quantity":150,"category":"grocery"},{"id":103,"description":"Radio AM/FM","price":25.49,"quantity":5,"category":"consumables"},{"id":1004,"description":"This is a description","price":99.99,"quantity":100,"category":"clothes"},{"id":104,"description":"This is a description","price":99.99,"quantity":100,"category":"clothes"}]}

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
* [Official documentation of Pydantic](https://docs.pydantic.dev/)
* [Official documentation of Uvicorn](https://www.uvicorn.org/)
* [REST API status code](https://restfulapi.net/http-status-codes/)
* [REST API method](https://restfulapi.net/http-methods/)
* [cURL utility](https://curl.se/)
* [Best README.md Template](https://github.com/othneildrew/Best-README-Template/pull/73)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
