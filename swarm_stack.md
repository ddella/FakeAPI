# Docker Swarm Stack for FakeAPI

## Docker Swarm Stack commands

1. To start the FakeAPI server, just type the following command:

```sh
docker stack deploy -c docker-compose-stack.yml fakeapi
```
2. To stop the FakeAPI and Redis servers, just type the following command:

```sh
docker stack rm fakeapi
```

## Docker Swarm stack
The `docker-compose-stack.yml` file to start multiple copies of FakeAPI with the Redis database on a Docker Swarm.

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

<p align="left">(<a href="README.md">back to the main page</a>)</p>
