<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>

# What is FakeAPI

FakeAPI is a Python script that implements most of the REST API methods. Do not use it in a production deployment. The script does almost no verifications, to keep the code small. I build it to learn more about the concept of REST API and also to test some API Gateways, load balancer and reverse proxy, like [Nginx API Gateway](https://www.nginx.com/learn/api-gateway/) to name a few.

FakeAPI is based the [FastAPI](https://fastapi.tiangolo.com/) framework. I'm using [Uvicorn](https://www.uvicorn.org/) as the [ASGI](https://asgi.readthedocs.io/en/latest/) web server and [Pydantic](https://docs.pydantic.dev/) for data validation.

>FakeAPI implements only `JSON` objects and requires **Python 3.10+**

Take a look at the file `requirement.txt` for the Python modules required:

REST API methods implemented in FakeAPI are:
* **HTTP GET** to retrieve information
* **HTTP POST** to create a new resource
* **HTTP PUT** to make a complete update (all fields), if the item doesn't exists it is NOT added
* **HTTP DELETE** to delete a resource
* **HTTP PATCH** to make a partial update (only one field)
* **HTTP TRACE** server reply with the header received in the body of the 

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
pip3 install --upgrade pip
pip3 install fastapi uvicorn pydantic pydantic[email]
```
>**Note**: If you get the following error message, it has nothing to do with Python, Pydantic, or your virtual environment. It's a `zsh` shell error.

    (.venv) user@MacBook src % pip3 install pydantic[email]
    zsh: no matches found: pydantic[email]

To avoid this, you can simply put the argument in quotes like this:
```sh
pip install 'pydantic[email]'
```

4. Create the `requirements.txt` file needed to build the image: 
```sh
pip3 freeze > requirements.txt
```

5. Make sure you're using the right Python interpreter, the one in the virtual environment:
```sh
(.venv) % which python3
```

The result should be something similar to this (your milage may vary 😀):
```
/Users/username/.../.venv/bin/python3
```

6. Start the app with the command:
```sh
python3 main.py
```

<a name="docker-container"></a>

# How to use this image (This is for educational **only**!)
## Build the Docker image

This is the `Dockerfile` to build the image:
```Dockerfilepych
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
```

This command builds the Docker image:

```sh
docker build -t fakeapi .
```

>The image should be `~85Mb`.
```sh
docker image ls fakeapi
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

# Run the project
>**Note**: This project is about REST API and not databases. The data is saved in a simple `json` file and is mapped outside the container on the Docker host. Multiple containers can use the same file but at some point disaster is not too far away 😀 In real life, we should have used a database, like [MongoDB](https://www.mongodb.com/).   

Use an appropriate `hostname` if you start multiple containers. The logs will print the `hostname`. That will help identify the container you are hitting, in case you have a load balancer. Remember my primary goal is to test API Gateways, Reverse Proxy and load balancer.

## Run the project with HTTP
The data will be located on the Docker host in the directory you start the container.

```sh
docker run -d --rm -v $PWD:/usr/src/data \
-e FAKEAPI_DATABASE=/usr/src/data/data.json \
-e FAKEAPI_INTF=0.0.0.0 \
-e FAKEAPI_PORT=8000 \
--name server1 --hostname server1 --network backend -p8000:8000 \
fakeapi
```
>If you prefer Docker Compose, see [FakeAPI YAML](FakeAPI_YAML.md)

## Run the project with HTTPS
This tutorial is not about OpenSSL. To use FakeAPI with HTTPS, you will need to generate a private key and a certificate. Check my tutorial on [OpenSSL](https://github.com/ddella/OpenSSL).

```sh
docker run -d --rm -v $PWD:/usr/src/data \
-e FAKEAPI_DATABASE=/usr/src/data/data.json \
-e FAKEAPI_USR_DATABASE=/usr/src/data/users.json \
-e FAKEAPI_INTF=0.0.0.0 \
-e FAKEAPI_PORT=9443 \
-e FAKEAPI_SERVER_KEY=server-key.pem \
-e FAKEAPI_SERVER_CRT=server-crt.pem \
--name server1 --hostname server1 --network backend -p 8000:9443 \
fakeapi
```
>**Note**: Don't forget to trust your CA in your trusted store if you decide to your own CA. On macOS, this is in KeyChain.

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

# let's get our hands dirty
The best way to test the APIs is with [cURL](https://curl.se/). Look at the documentation from swagger. A cURL example is included with every function. 

## Example with GET method
Use this command to query all the objects in the database:

```sh
curl -H "Content-type: application/json" \
-H "Accept: application/json" \
-i -L "http://localhost:8000/api/items"
```
This will send a `GET` request to the server and it will return all the object in `JSON` format:

    HTTP/1.1 200 OK
    date: Sun, 01 Jan 2023 00:00:00 GMT
    server: uvicorn
    content-length: 613
    content-type: application/json

    {"message":"Root of Fake REST API","method":"GET","items":[{"id":100,"description":"This is a description","price":99.99,"quantity":100,"category":"clothes"},{"id":101,"description":"Jeans","price":39.99,"quantity":100,"category":"clothes"},{"id":102,"description":"Apple","price":0.5,"quantity":150,"category":"grocery"},{"id":103,"description":"Radio AM/FM","price":25.49,"quantity":5,"category":"consumables"},{"id":1004,"description":"This is a description","price":99.99,"quantity":100,"category":"clothes"},{"id":104,"description":"This is a description","price":99.99,"quantity":100,"category":"clothes"}]}

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License
Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact
Daniel Della-Noce - [Linkedin](https://www.linkedin.com/in/daniel-della-noce-2176b622/) - daniel@isociel.com

Project Link: [https://github.com/ddella/FakeAPI](https://github.com/ddella/FakeAPI)
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Acknowledgments
* [Official documentation of FastAPI](https://fastapi.tiangolo.com/)
* [Official documentation of Pydantic](https://docs.pydantic.dev/)
* [Official documentation of Uvicorn](https://www.uvicorn.org/)
* [REST API status code](https://restfulapi.net/http-status-codes/)
* [REST API method](https://restfulapi.net/http-methods/)
* [cURL utility](https://curl.se/)
* [Best README.md Template](https://github.com/othneildrew/Best-README-Template/pull/73)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
