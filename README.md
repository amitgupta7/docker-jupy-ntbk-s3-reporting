# docker-jupy-ntbk-s3-reporting
## Provided as-is (w/o support)
This is a docker container to run jupyter notebook for generating performance reports from s3. The AWS sso authentication is handled interactively upon running the container. This requires docker to build and run the container. 
## Installing docker (Prerequisite)
This uses docker to run the jupyter server. Use the following instructions to install docker-desktop:
* Mac Instructions: https://docs.docker.com/desktop/install/mac-install/ 
* Linux Instructions: https://docs.docker.com/desktop/install/linux-install/
* Windows Instructions: https://docs.docker.com/desktop/install/windows-install/ 
## Usage
Use the `make run` command to run the jupyter server on `http://127.0.0.1:8888/lab`. The `auth` and `sync` targets can be used when the jupyter server container is running to autheticate and sync with s3. Jupiter server password is hardcoded to `my-password`. 
```shell
git clone https://github.com/amitgupta7/docker-jupy-ntbk-s3-reporting.git
cd docker-jupy-ntbk-s3-reporting
## Build container image
make build 
## Run jupyter server in background on http://127.0.0.1:8888/lab
## Jupiter server password is set to 'my-password'
## use `make run` without `MODE="-d"`to run in verbose. 
make run MODE="-d"
## Authenticate and sync reports from s3 bucket
## auth and sync targets can also be run separately.
make auth sync
## To stop the jupyter server running in background
make stop
## Print usage
make
## USAGE: 
## make build                              Run docker image build
## make run                                Run jupyter server without any s3 sync.
## make auth                               Authenticate aws cli with web sso.
## make sync                               Run aws s3 sync on .dataDir
## make run-with-full-s3-download          Authenticate/sync aws-s3 with web sso before starting jupyter server (slow).
```
Alternatively, `run-with-full-s3-download` target may be used to perform s3 download (could be 10s of GB data) during the run jupyter server. 
```shell
git clone https://github.com/amitgupta7/docker-jupy-ntbk-s3-reporting.git
cd team-cx-tools/docker-jupy-ntbk-s3-reporting
make build run-with-full-s3-download
## follow the instructions on prompt to authenticate with aws sso and run the jupiter server on http://127.0.0.1:8888/lab
## Jupiter server password is set to 'my-password'
```
## Stop Jupyter server
Hit 'ctrl+c' and then 'y' to stop the server. Hit 'ctrl+c' twice shuts down the Server and immediately destroys the Docker container. Alternatively, `make stop` command will stop any running jupyter server containers. 
```shell
##output
# Setting password for jupyter server to 'my-password'
# .....
# [I 2024-07-30 13:55:02.091 ServerApp] Jupyter Server 2.14.1 is running at:
# [I 2024-07-30 13:55:02.091 ServerApp] http://3a971ca067c7:8888/lab
# [I 2024-07-30 13:55:02.091 ServerApp]     http://127.0.0.1:8888/lab
# [I 2024-07-30 13:55:02.091 ServerApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
## Hit 'ctrl+c' and then 'y' to stop the server.
# Shut down this Jupyter server (y/[n])? y
## Pressing 'Ctrl-C' twice shuts down the Server and immediately destroys the Docker container. 
```
## Installing dependencies
Dependencies may be specified in `Dockerfile`. The default Python 3.x Conda environment resides in /opt/conda. See [common features](https://github.com/jupyter/docker-stacks/blob/main/docs/using/common.md#conda-environments) for more information. 
