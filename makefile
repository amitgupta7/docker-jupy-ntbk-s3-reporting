IMG=jupy-ntbk-s3-reporting
VER=latest
build: preflight
	docker build -t ${IMG}:${VER} .
run: preflight
	docker run -p 8888:8888 --rm -v "${PWD}":/home/jovyan -it ${IMG}:${VER}
preflight:
	@echo "checking ..."
	@type docker >/dev/null 2>&1 || { echo >&2 "docker is not installed.  Aborting."; exit 1; }
	@echo "docker is installed."