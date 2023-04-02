# Docker Swarm Stack for FakeAPI

## What is a swarm?
The cluster management and orchestration features embedded in the Docker Engine are built using swarmkit. Swarmkit is a separate project which implements Docker’s orchestration layer and is used directly within Docker.

A swarm consists of multiple Docker hosts which run in swarm mode and act as managers (to manage membership and delegation) and workers (which run swarm services). A given Docker host can be a manager, a worker, or perform both roles. When you create a service, you define its optimal state (number of replicas, network and storage resources available to it, ports the service exposes to the outside world, and more). Docker works to maintain that desired state. For instance, if a worker node becomes unavailable, Docker schedules that node’s tasks on other nodes. A task is a running container which is part of a swarm service and managed by a swarm manager, as opposed to a standalone container.

One of the key advantages of swarm services over standalone containers is that you can modify a service’s configuration, including the networks and volumes it is connected to, without the need to manually restart the service. Docker will update the configuration, stop the service tasks with the out of date configuration, and create new ones matching the desired configuration.

>When Docker is running in swarm mode, you can still run standalone containers on any of the Docker hosts participating in the swarm, as well as swarm services. A key difference between standalone containers and swarm services is that only swarm managers can manage a swarm, while standalone containers can be started on any daemon.

## Docker Swarm Stack commands

1. To start the FakeAPI and Redis containers in a Docker Swarm as a stack, type the following command:

```sh
docker stack deploy -c docker-compose-stack.yml fakeapi
```
2. To stop the stack of FakeAPI and Redis containers in a Docker Swarm, type the following command:

```sh
docker stack rm fakeapi
```

## Docker Swarm stack
The `docker-compose-stack.yml` file to start multiple copies of FakeAPI with one Redis database on a Docker Swarm.

```yaml
# Start the container(s): docker stack deploy -c docker-compose-stack.yml fakeapi
# Stop the container(s): docker stack rm fakeapi
#
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
    domainname: backend.com
    image: fakeapi
    ports:
      - "9445:9445"
    deploy:
      replicas: 6
    environment:
      - REDIS_HOSTNAME=redis.lab
      - REDIS_PORT=6379
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
    domainname: backend.com
    networks:
       backend:
```

Somme commands to check the Swarm stack:
```sh
docker stack ls
docker stack ps fakeapi
docker stack services fakeapi
```

<p align="left">(<a href="README.md">back to the main page</a>)</p>
