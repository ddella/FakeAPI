# Docker Compose for the FakeAPI container

## Docker Compose commands

This is the `yaml` file to run the FakeAPI Server detached.

1. To start the FakeAPI server, just type the following command:

```sh
docker compose -f fakeapi.yml --project-name fakeapi up -d
```
2. To stop the FakeAPI server, just type the following command:

```sh
docker container rm -f server1
```

## YAML file to start the FakeAPI Server

```yaml
# fakeapi.yml
# Start the container: docker compose -f fakeapi.yml --project-name fakeapi up -d
# Stop the container: docker container rm -f server1
networks:
   backend:
      name: backend

services:
  fakeapi1:
    image: fakeapi
    volumes:
      - type: bind
        source: $PWD
        target: /usr/src/data
        # read_only: true
    ports:
      - "8000:8000"
    restart: unless-stopped
    environment:
      - FAKEAPI_DATABASE=/usr/src/data/data.json
      - FAKEAPI_INTF=0.0.0.0
      - FAKEAPI_PORT=8000
    container_name: server1
    hostname: server1
    domainname: backend.com
    networks:
      backend:
        ipv4_address: 172.31.11.11
```

## Useful Links

- [The Compose Specification](https://github.com/compose-spec/compose-spec/blob/master/spec.md)
