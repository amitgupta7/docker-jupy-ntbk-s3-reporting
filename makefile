$(VERBOSE).SILENT:
IMG=jupy-ntbk-s3-reporting
VER=latest
NAME=jupy-ntbk-s3
usage:
	echo "USAGE: See "
	echo "make build				Run docker image build"
	echo "make run-with-s3-sync			Authenticate/sync aws-s3 with web sso."
	echo "make run				Run jupyter server without s3 sync."
build: preflight
	docker build -t ${IMG}:${VER} .
run: preflight
	docker run --name ${NAME} -p 8888:8888 --rm -v "${PWD}":/home/jovyan -it ${IMG}:${VER}
run-with-s3-sync: preflight
	docker run --name ${NAME} -e SYNC_S3="true" -p 8888:8888 --rm -v "${PWD}":/home/jovyan -it ${IMG}:${VER}
preflight:
	echo "checking ..."
	type docker >/dev/null 2>&1 || { echo >&2 "docker is not installed.  Aborting."; exit 1; }
	echo "docker is installed."	