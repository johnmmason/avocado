NAME ?= phart

all: ps-me im-me

im-me:
	docker images | grep ${NAME}
ps-me:
	docker ps -a | grep ${NAME}
build-worker:
	docker build -f <dockerfile path>  -t <tagname:version> .

build-all: build-worker build-api build-db


run-wrk: build-wrk
	docker run --name <name> --network <docker bridge networking> -p <my redis port>:6379 -d --env REDIS_IP=<name> -u <> -v ${PWD}/data:/data <name of image>

run-all: run-db run-api run-wrk



clean-wrk:
	docker rm -f <contianer name>

clean-db:
	docker rm -f <container name>

clean-api:
	docker rm -f <container name>


clean-all: clean-db clean-api clean-wrk
