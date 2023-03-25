# Docker Compose for the FakeAPI container

## Docker Compose commands

This is the `yaml` file to run the FakeAPI Server detached.

1. To start the FakeAPI server, just type the following command:

```sh
docker compose -f fakeapi.yml --project-name fakeapi up -d
```
2. To stop the FakeAPI server, just type the following command:

```sh
docker container rm -f fakeapi10
```

## YAML file to start the FakeAPI Server

```yaml
# fakeapi.yml
# Start the container: docker compose -f fakeapi.yml --project-name fakeapi up -d
# Stop the container: docker container rm -f sefakeapi10rver1
networks:
   backend:
      name: backend

services:
  fakeapi10:
    image: fakeapi
    volumes:
      - type: bind
        source: $PWD
        target: /usr/src/data
    ports:
      - "8000:8000"
    restart: unless-stopped
    environment:
      - HOST=172.31.11.10
      - PORT=8000
    hostname: fakeapi10
    container_name: fakeapi10
    domainname: example.com
    networks:
      backend:
        ipv4_address: 172.31.11.10
```

## Useful Links

- [The Compose Specification](https://github.com/compose-spec/compose-spec/blob/master/spec.md)
