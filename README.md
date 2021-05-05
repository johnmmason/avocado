# avocado

## Usage

Our system supports a variety of actions (jobs) which interact with and run analysis on our dataset.  All jobs must be submitted to our API where they are queued for processing by worker nodes.

The following job types are supported:

* Insert
* Query
* Update
* Delete
* Plot
* Summary

### Preferred Method: Web Application

Our web application can be accessed at https://isp-proxy.tacc.utexas.edu/phart/.

### Alternate Method: Interact directly with our API

If you prefer to submit jobs in raw JSON format, you can do so using the `raw_jobs` route.  See `avocado/worker/README.md` for proper job formatting and examples.

Jobs can be sent via POST request using curl or a program like Postman.

```
curl -X POST -H "content-type: application/json" -d '{"job_type": "sample"}' https://isp-proxy.tacc.utexas.edu/phart/raw_jobs
```

## Deployment Instructions

### Production Deployment Instructions (Kubernetes)

Section in progress...

### Test Deployment Instructions (docker-compose)

For rapid testing and development, the project can be launched using docker-compose.

Use the `-d` flag to run in the daemon mode and the `--build` flag to rebuild the containers on launch (optional).

```
docker-compose up -d --build
...
Starting avocado_redis_1    ... done
Starting avocado_postgres_1 ... done
Starting avocado_api_1      ... done
Starting avocado_worker_1   ... done
```

To launch multiple workers, add `--scale worker={num_workers}`

```
docker-compose up -d --scale worker=3
Starting avocado_redis_1    ... done
Starting avocado_postgres_1 ... done
Starting avocado_api_1      ... done
Starting avocado_worker_1   ... done
Starting avocado_worker_2   ... done
...
```
