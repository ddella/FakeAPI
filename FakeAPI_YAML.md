# Docker Compose for the FakeAPI container

### YAML file to start the FakeAPI Server

This is the `yaml` file to run the FakeAPI Server detached.

To start the FakeAPI server, just type the following command, with the file `fakeapi.yml`.

```command
docker compose -f fakeapi.yml --project-name fakeapi up -d
```

```yaml
# filename: fakeapi.yml
# docker compose -f fakeapi.yml --project-name fakeapi up -d
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
      - "9443:9443"
    restart: unless-stopped
    environment:
      - HOST=172.31.11.10
      - PORT=9443
    hostname: fakeapi10
    container_name: fakeapi10
    domainname: example.com
    networks:
      backend:
        ipv4_address: 172.31.11.10
```

## Useful Links

- [The Compose Specification](https://github.com/compose-spec/compose-spec/blob/master/spec.md)
