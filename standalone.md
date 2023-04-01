<a name="readme-top"></a>

# Run a standalone container of FakeAPI and Redis
Start the fakeAPI and Redis servers in a custom network, to have Docker's DNS for name resolution. In this example I'm using the network `backend`. Use an appropriate `hostname` if you start multiple containers. The logs will print the `hostname`. That will help identify the container you are hitting, in case you have a load balancer. Remember my primary goal is to test API Gateways, Reverse Proxy and load balancer.

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
fakeapi:2.0
```
>**Note**: Don't forget to trust your CA in your trusted store if you decide to your own CA. On macOS, this is in KeyChain.

## Redis
Start Redis with the following command:
```sh
docker run --name redis.lab --hostname redis.lab -d --rm --network backend redis
```
>**Note**: No need to map the Redis port on the Docker host, since it's only accessed by the FakeAPI. In case you want to expose the port, add `-p 6379:6379` to the command line.

**Optional:** You can start a Redis client for troubleshooting the Redis database. Note that the hostname is 'redis.lab' because we're in the same network as the server. Don't use 'localhost' as this container is in the same network as the Redis server and Docker's DNS will take care of the name resolution:
```sh
docker run -it --rm --network backend --name redis.cli redis redis-cli -h redis.lab
```

## Custom network (optional)
FakeAPI runs on a custom Docker network. This workshop is not about Docker custom network but I encourage you to run your containers in custom networks to get the added value of a DNS server. The following command was used to create the `backend` network.

```sh
docker network create --driver=bridge --subnet=172.31.11.0/24 --ip-range=172.31.11.128/25 --gateway=172.31.11.1 backend
```
<p align="left">(<a href="README.md">back to the main page</a>)</p>
