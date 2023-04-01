<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>

# What is FakeAPI

FakeAPI is a Python script that implements most of the REST API methods. Do not use it in a production deployment. The script does almost no verifications, to keep the code small. I build it to learn more about the concept of REST API and also to test some API Gateways, load balancer and reverse proxy, like [Nginx API Gateway](https://www.nginx.com/learn/api-gateway/) to name a few.

FakeAPI is based the [FastAPI](https://fastapi.tiangolo.com/) framework. I'm using [Uvicorn](https://www.uvicorn.org/) as the [ASGI](https://asgi.readthedocs.io/en/latest/) web server and [Pydantic](https://docs.pydantic.dev/) for data validation. All the data is saved in a Redis database.

>FakeAPI implements only `JSON` objects and requires **Python 3.10+**

Take a look at the file `requirement.txt` for the Python modules required:

REST API methods implemented in FakeAPI are:
* **HTTP GET** to retrieve information
* **HTTP POST** to create a new resource
* **HTTP PUT** to make a complete update (all fields), if the item doesn't exists it is NOT added
* **HTTP DELETE** to delete a resource
* **HTTP PATCH** to make a partial update (only one field)
* **HTTP TRACE** server reply with the header received in the body of the 

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

>The image should be `~135Mb`.
```sh
docker image ls fakeapi
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

# Run the project
Start the fakeAPI and Redis servers in a custom network, to have Docker's DNS for name resolution.  

Use an appropriate `hostname` if you start multiple containers. The logs will print the `hostname`. That will help identify the container you are hitting, in case you have a load balancer. Remember my primary goal is to test API Gateways, Reverse Proxy and load balancer.

## Run the project with HTTP
Starts the container with `HTTP` only.

```sh
docker run -d --rm \
-e REDIS_HOSTNAME=redis.lab \
-e REDIS_PORT=6379 \
-e FAKEAPI_INTF=0.0.0.0 \
-e FAKEAPI_PORT=8000 \
--name server1 --hostname server1 --network backend -p8000:8000 \
fakeapi
```
>If you prefer Docker Compose, see [FakeAPI YAML](FakeAPI_YAML.md)

## Run the project with HTTPS
This tutorial is not about OpenSSL. To use FakeAPI with `HTTPS`, you will need to generate a private key and a certificate. Check my tutorial on [OpenSSL](https://github.com/ddella/OpenSSL). I've included a private key and a self signed certificate.

```sh
docker run -d --rm \
-e REDIS_HOSTNAME=redis.lab \
-e REDIS_PORT=6379 \
-e FAKEAPI_INTF=0.0.0.0 \
-e FAKEAPI_PORT=9443 \
-e FAKEAPI_SERVER_KEY=server-key.pem \
-e FAKEAPI_SERVER_CRT=server-crt.pem \
--name server1 --hostname server1 --network backend -p 9443:9443 \
fakeapi
```
>**Note**: Don't forget to trust your CA in your trusted store if you decide to your own CA. On macOS, this is in KeyChain.

### Redis
Start Redis with the following command:
```sh
docker run --name redis.lab --hostname redis.lab -d --rm --network backend redis
```
>**Note**: No need to map the Redis port on the Docker host, since it's only accessed by the FakeAPI. In case you want to expose the port, add `-p 6379:6379` to the command line.

**Optional:** You can start a Redis client for troubleshooting. Note that the hostname is 'redis.lab' because we're in the same network as the server. Don't use 'localhost' as this container is in the same network as the Redis server and Docker's DNS will take care of resolution:
```sh
docker run -it --rm --network backend redis redis-cli -h redis.lab
```

## Custom network (optional)
FakeAPI runs on a custom Docker network. This workshop is not about Docker custom network but I encourage you to run your containers in custom networks to get the added value of a DNS server. The following command was used to create the `backend` network.

```sh
docker network create --driver=bridge --subnet=172.31.11.0/24 --ip-range=172.31.11.128/25 --gateway=172.31.11.1 backend
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

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

## Development
If you want to plya with the source code, you can read the following tutorial to setup a Python development environment

* [development](dev.md)

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
