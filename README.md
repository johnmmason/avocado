# avocado

#### Docker Build Commands

```
[avocado]$ docker build --file docker/Dockerfile.api --tag avocado/api:latest .
[avocado]$ docker build --file docker/Dockerfile.wrk --tag avocado/worker:latest .
[avocado]$ docker build --file docker/Dockerfile.db --tag avocado/redis_db:latest .
```

#### Docker Run Commands

In order for networking to work correctly in the test environment (Docker), we use docker-compose to launch our containers:

```
[avocado]$ docker-compose up -d
```

**NOTE:** This is an incomplete solution. Container images need to be re-built before launching with docker-compose. We should discuss changes which would allow docker-compose to build images automatically.
