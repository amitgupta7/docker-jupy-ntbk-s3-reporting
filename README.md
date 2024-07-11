#docker-jupy-ntbk-s3-reporting
## Provided as-is (w/o support)
This is a docker container to run jupyter notebook for generating performance reports from s3. The AWS sso authentication is handled interactively upon running the container. This requires docker to build and run the container. 

## Usage
```shell
git clone https://github.com/amitgupta7/docker-jupy-ntbk-s3-reporting
cd docker-jupy-ntbk-s3-reporting
make
make run
## follow the instructions on prompt to run the jupiter server on http://127.0.0.1:8888/lab
```
## Installing docker
Mac Instructions: https://docs.docker.com/desktop/install/mac-install/ 
Linux Instructions: https://docs.docker.com/desktop/install/linux-install/
