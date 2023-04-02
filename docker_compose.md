# Docker Compose for FakeAPI and Redis services
Compose is a tool for defining and running multi-container Docker applications. With Compose, you use a `YAML` file to configure your application’s services. Then, with a single command, you create and start all the services from your configuration.

Using Compose is essentially a three-step process:

1. Define your app’s environment with a `Dockerfile` so it can be reproduced anywhere. (refer to the main page to build the image)
2. Define the services that make up your app in `docker-compose.yml` so they can be run together in an isolated environment.
3. Run docker compose up and the Docker compose command starts and runs your entire app.

>Step 1 was already covered at the beginning of the tutorial

## Docker Compose commands to start the FakeAPI Server
This is the `yaml` file to run the FakeAPI Server detached.

1. To start the FakeAPI environment, just type the following command:

```sh
docker compose -f docker-compose.yml --project-name fakeapi up -d
```
>This will start one FakeAPI and one Redis container

2. To stop the FakeAPI and Redis servers, just type the following command:

```sh
docker compose rm -f -s fakeapi redis
```
>This will stop both containers that were started above

## YAML file to start the FakeAPI Server
The `docker-compose.yml` file:

```yaml
# docker-compose.yml
# Start the container(s): docker compose -f docker-compose.yml --project-name fakeapi up -d
# Stop the container(s): docker compose rm -f -s fakeapi redis
version: "3.9"
networks:
   backend:
      name: backend
services:
  fakeapi:
    image: fakeapi:2.0
    ports:
      - "8000:8000"
    restart: unless-stopped
    environment:
      - REDIS_HOSTNAME=redis.lab
      - REDIS_PORT=6379
      - FAKEAPI_INTF=0.0.0.0
      - FAKEAPI_PORT=8000
      - FAKEAPI_SERVER_KEY=server-key.pem
      - FAKEAPI_SERVER_CRT=server-crt.pem
    container_name: server1
    hostname: server1
    domainname: backend.com
    networks:
      backend:

  redis:
    image: redis:alpine
    deploy:
      replicas: 1
    container_name: redis.lab
    hostname: redis.lab
    domainname: backend.com
    networks:
       backend:
```
## Logging
In case you run into problems, you can start logging with the command:
```sh
docker logs -f server1
```
<p align="left">(<a href="README.md">back to the main page</a>)</p>

## Redis Client (*Optional*)
You can start a Redis client for troubleshooting the Redis container. Note that the hostname, on the command line, to access the Redis server is `redis.lab` because we're in the same network as the Redis server.
```sh
docker run -it --rm --network backend --name redis.cli redis redis-cli -h redis.lab
```

<p align="left">(<a href="README.md">back to the main page</a>)</p>
