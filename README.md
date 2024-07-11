#docker-jupy-ntbk-s3-reporting
## Provided as-is (w/o support)
This is a docker container to run jupyter notebook for generating performance reports from s3. The AWS sso authentication is handled interactively upon running the container. This requires docker to build and run the container. 

## Installing docker (Prerequisite)
* Mac Instructions: https://docs.docker.com/desktop/install/mac-install/ 
* Linux Instructions: https://docs.docker.com/desktop/install/linux-install/

## Usage
```shell
git clone https://github.com/amitgupta7/docker-jupy-ntbk-s3-reporting
cd docker-jupy-ntbk-s3-reporting
make
make run
## follow the instructions on prompt to authenticate with aws sso and run the jupiter server on http://127.0.0.1:8888/lab
```
When the container is running, it can be accessed with the `docker exec` command. The `make sync-s3` command will run the s3 sync again to download any missing/new files from aws s3.

```shell
make run
## when container is running, run make sync-s3 ...
make sync-s3
## Output
# resyncing s3 ...
# download: s3://....
```