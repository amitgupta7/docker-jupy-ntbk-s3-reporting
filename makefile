$(VERBOSE).SILENT:
IMG=jupy-ntbk-s3-reporting
VER=latest
NAME=jupy-ntbk-s3
build: preflight
	docker build -t ${IMG}:${VER} .
run: preflight
	docker run --name ${NAME} -p 8888:8888 --rm -v "${PWD}":/home/jovyan -it ${IMG}:${VER}
preflight:
	echo "checking ..."
	type docker >/dev/null 2>&1 || { echo >&2 "docker is not installed.  Aborting."; exit 1; }
	echo "docker is installed."
sync-s3:
	echo "resyncing s3 ..."
	docker exec -it ${NAME} aws s3 sync s3://securiti-state-718391394098/cx/ .dataDir