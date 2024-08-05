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
make build run-with-s3-sync
## follow the instructions on prompt to authenticate with aws sso and run the jupiter server on http://127.0.0.1:8888/lab
## Jupiter server password is set to 'my-password'
```
If s3 sync is not required, use the `make run` command instead. 

## Stop Jupyter server
Hit 'ctrl+c' and then 'y' to stop the server. Hit 'ctrl+c' twice shuts down the Server and immediately destroys the Docker container. 
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
