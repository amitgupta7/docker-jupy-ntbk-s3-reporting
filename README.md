# docker-jupy-ntbk-s3-reporting
## Provided as-is (w/o support)
This is a docker container to run jupyter notebook for generating performance reports from s3. The AWS sso authentication is handled interactively upon running the container. This requires docker to build and run the container. 
## Installing docker (Prerequisite)
* Mac Instructions: https://docs.docker.com/desktop/install/mac-install/ 
* Linux Instructions: https://docs.docker.com/desktop/install/linux-install/
## Usage
```shell
git clone git@bitbucket.org:securitiai/team-cx-tools.git
cd team-cx-tools/docker-jupy-ntbk-s3-reporting
make build run-with-full-s3-download
## follow the instructions on prompt to authenticate with aws sso and run the jupiter server on http://127.0.0.1:8888/lab
## Jupiter server password is set to 'my-password'
```
Alternatively, s3 sync is not required to run the jupyter server. Use the `make run` command to run the jupyter server without s3 sync. `s3-auth` and `s3-sync` targets may be used when the jupyter server container is running to re-sync with s3.
```shell
## Run jupyter server in background
make build run 2>/dev/null & 
## Authenticate and sync reports from s3 bucket
make auth sync
## To stop the jupyter server running in background
make stop
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

