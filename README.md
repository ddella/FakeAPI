<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>

# What is FakeAPI

FakeAPI is a Python script that implements most of the REST API methods. Do not use it in a production deployment. The script does almost no verifications, to keep the code small. I build it to learn more about the concept of REST API and also to test some API Gateways, load balancer and reverse proxy, like [Nginx API Gateway](https://www.nginx.com/learn/api-gateway/) to name a few. The data is saved in a Redis database.

FakeAPI is based on:
* [FastAPI](https://fastapi.tiangolo.com/) framework
* [Uvicorn](https://www.uvicorn.org/) as the [ASGI](https://asgi.readthedocs.io/en/latest/) web server
* [Pydantic](https://docs.pydantic.dev/) for data validation
* [Redis](https://redis.io)

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

This is the `Dockerfile` needed to build the Docker image:
```Dockerfile
# Use the following command to build the Docker image:
#   docker build -t fakeapi .
# (Optional) If you suspect somethings wrong, you can start the container with the command:
#   docker run -it --rm --name fakeapi fakeapi /bin/sh
#
FROM python:alpine

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

Use this command to build the Docker image:
```sh
docker build -t fakeapi:2.0 .
```

>The image should be `~135Mb`.
```sh
docker image ls fakeapi:2.0
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

# Run the project
The FakeAPI project is meant to run as Docker containers.

1. Run a standalone container of FakeAPI and Redis [standalone](standalone.md)
2. Run a standalone container of FakeAPI and Redis with Docker Compose [Docker Compose](docker_compose.md)
3. Run all containers as a Stack in a Docker Swarm [Docker Swarm Stack](swarm_stack.md)

## Docker Swarm stack
This is a `YAML` file to start multiple copies of FakeAPI with the Redis database on a Docker Swarm

```yaml
# docker stack deploy -c docker-compose-stack.yml fakeapi
# Create the network, on the manager node **ONLY**
#   docker network create -d overlay --subnet=172.21.5.0/24 \
#   --gateway=172.21.5.1 --ip-range 172.21.5.224/27 --attachable ovrl_stack_fakeapi
version: "3.9"
networks:
   backend:
      name: ovrl_stack_fakeapi
      external: true

services:
  fakeapi:
    hostname: "{{.Service.Name}}-{{.Node.ID}}"
    image: fakeapi
    ports:
      - "9445:9445"
    deploy:
      replicas: 6
    environment:
      - REDIS_HOSTNAME=redis.lab \
      - REDIS_PORT=6379 \
      - FAKEAPI_INTF=0.0.0.0
      - FAKEAPI_PORT=9445
      - FAKEAPI_SERVER_KEY=server-key.pem
      - FAKEAPI_SERVER_CRT=server-crt.pem
    networks:
      - backend

  redis:
    image: redis:alpine
    deploy:
      replicas: 1
    hostname: redis.lab
    networks:
       backend:
```

Somme commands to check the Swarm stack

```sh
docker stack deploy --compose-file docker-compose-stack.yml fakeapi
docker stack ls
docker stack ps fakeapi
docker stack rm fakeapi
docker stack services fakeapi
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
