# Docker Compose for the FakeAPI container

## Docker Compose commands to start the FakeAPI Server
This is the `yaml` file to run the FakeAPI Server detached.

1. To start the FakeAPI server, just type the following command:

```sh
docker compose -f docker-compose.yml --project-name fakeapi up -d
```
2. To stop the FakeAPI and Redis servers, just type the following command:

```sh
docker container rm -f server1 redis.lab
```

## YAML file to start the FakeAPI Server
The `docker-compose.yml` file:

```yaml
# docker-compose.yml
# Start the container: docker compose -f docker-compose.yml --project-name fakeapi up -d
# Stop the container: docker container rm -f server1 redis.lab
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
    hostname: redis.lab
    container_name: redis.lab
    networks:
       backend:
```
<p align="left">(<a href="README.md">back to the main page</a>)</p>

## Logging
In case you run into problems, you can start logging with the command:
```sh
docker logs -f server1
```
<p align="left">(<a href="README.md">back to the main page</a>)</p>
