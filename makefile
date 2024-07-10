IMG=jupy-ntbk-s3-reporting
VER=latest
build:
	docker build -t ${IMG}:${VER} .
run: 
	docker run -p 8888:8888 --rm -v "${PWD}":/home/jovyan -it ${IMG}:${VER}