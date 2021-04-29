# avocado

#### Docker Build Commands

Run using the Makefile and a docker compose
```
make build-all
docker-compose up
```
#### Curl command to POST a job request

```
curl -X POST -H "content-type: application/json" -d '{<JSON String to do PostGres CRUD operation>}' localhost:5012/jobs
```

#### Testing job update/completion in Redis DB

Open a python shell to run the following redis commands

```
Python 3.6.8 (default, Aug  7 2019, 17:28:10)
[GCC 4.8.5 20150623 (Red Hat 4.8.5-39)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import redis
>>> rd=redis.StrictRedis(host='localhost', port=6392, db=10)
>>> rd.keys()
[b'job.50738e81-fa4c-443a-9e8e-ef64cf02077b']
>>> rd.get('job.50738e81-fa4c-443a-9e8e-ef64cf02077b')
b'{"job_type": "insert", "status": "complete", "end": "2021-04-28 22:25:56.425080"}'
```
