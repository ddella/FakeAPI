<a name="readme-top"></a>

# Run a standalone FakeAPI and Redis container
Start the FakeAPI and Redis containers in a custom network, to have Docker's DNS for name resolution. In this example. the network is `backend`. Use an appropriate `hostname` if you start multiple containers. The logs and page visited will print the `hostname`. That will help identify the container you are hitting, in case you have a load balancer. Remember my primary goal is to test API Gateways, Reverse Proxy and load balancer.

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

## Run the project with HTTPS
This tutorial is not about OpenSSL. To use FakeAPI with `HTTPS`, you will need to generate a private key and a certificate. Check my tutorial on [OpenSSL](https://github.com/ddella/OpenSSL). I've included a private key and a certificate signed by a private CA.

```sh
docker run -d --rm \
-e REDIS_HOSTNAME=redis.lab \
-e REDIS_PORT=6379 \
-e FAKEAPI_INTF=0.0.0.0 \
-e FAKEAPI_PORT=8000 \
-e FAKEAPI_SERVER_KEY=server-key.pem \
-e FAKEAPI_SERVER_CRT=server-crt.pem \
--name server1 --hostname server1 --network backend -p 8000:8000 \
fakeapi:2.0
```
>**Note**: Don't forget to trust your CA in your trusted store if you decide to your own CA. On macOS, this is in KeyChain.

<p align="left">(<a href="README.md">back to the main page</a>)</p>

## Redis
To start a Redis container running in the background, use the following command:
```sh
docker run --name redis.lab --hostname redis.lab -d --rm --network backend -p 6379:6379 redis
```

To start a Redis container with interactive shell and many rarely useful info, use the following command:
```sh
docker run --name redis.lab --hostname redis.lab -it --rm --network backend -p 6379:6379 redis --loglevel verbose
```

>**Note**: You don't need to map the Redis port on the Docker host. The Redis server is only accessed by the FakeAPI containers. In case you want to expose the Redis port to the outside world, add `-p 6379:6379` to the command line.

**Optional:** You can start a Redis client for troubleshooting the Redis container. Note that the hostname, on the command line, to access the Redis server is `redis.lab` because we're in the same network as the Redis server.
```sh
docker run -it --rm --network backend --name redis.cli redis redis-cli -h redis.lab
```

## Custom network
FakeAPI runs on a custom Docker network to get the added value of Docker DNS server. The following command was used to create the `backend` network use througth this example.

```sh
docker network create --driver=bridge --subnet=172.31.11.0/24 --ip-range=172.31.11.128/25 --gateway=172.31.11.1 backend
```
## Logging
In case you run into problems, you can start logging with the command:
```sh
docker logs -f server1
```

>FakeAPI is quite verbose

## Inside the container (Optional)
In case you want to go inside the container, you can start a shell with the command:
```sh
docker exec -it --rm server1 /bin/sh
```

<p align="left">(<a href="README.md">back to the main page</a>)</p>
