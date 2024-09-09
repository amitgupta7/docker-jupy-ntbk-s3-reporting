$(VERBOSE).SILENT:
export DOCKER_CLI_HINTS=false
IMG=jupy-ntbk-s3-reporting
VER=latest
NAME=jupy-ntbk-s3
datadir=.dataDir
usage:
	echo "USAGE: See "
	echo "make build				Run docker image build"
	echo "make run				Run jupyter server without any s3 sync."
	echo "make auth				Authenticate aws cli with web sso."
	echo "make sync				Run aws s3 sync on .dataDir"
	echo "make run-with-full-s3-download		Authenticate/sync aws-s3 with web sso before starting jupyter server (slow)."
build: preflight
	docker build -t ${IMG}:${VER} .
run: preflight
	docker run --name ${NAME} -p 8888:8888 --rm -v "${PWD}":/home/jovyan -it ${IMG}:${VER}
sync: container-check
	echo "syncing with s3 with --size-only option, file creation date will be ignired."
	docker exec -it ${NAME}	mkdir -p ${datadir}
	docker exec -it ${NAME} aws s3 sync --size-only s3://securiti-cx-exports/cx/ ${datadir}
run-with-full-s3-download: preflight
	docker run --name ${NAME} -e SYNC_S3="true" -p 8888:8888 --rm -v "${PWD}":/home/jovyan -it ${IMG}:${VER}
preflight:
	printf '%s' "checking ..."
	type docker >/dev/null 2>&1 || { echo >&2 "docker is not installed.  Aborting."; exit 1; }
	echo "docker is installed."	
container-check: preflight
	@if [ $$(docker container inspect -f '{{.State.Running}}' ${NAME} 2>/dev/null) == "true" ]; then\
        echo "Jupyter server container is running";\
	else\
		echo "Jupyter server container is NOT running. Aborting.";\
    fi
auth: container-check
	docker exec -it ${NAME}	mkdir -p ~/.aws
	docker exec -it ${NAME}	cp config ~/.aws
	docker exec -it ${NAME}	aws sso login --no-browser
stop: 
	echo "Waiting for container ${NAME}..."
	docker stop ${NAME}