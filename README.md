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

## Stop Jupyter server
```shell
make run

##output
# Alternatively, you may visit the following URL which will autofill the code upon loading:
# https://device.sso.us-west-2.amazonaws.com/?user_code=SFCC-NRCC
# Successfully logged into Start URL: https://securiti.awsapps.com/start/#
# download: s3://...
#    Jupyter Server 2.14.1 is running at:
#     http://59c9b717a091:8888/lab?token=2da6189e776bc61c2674a14ef1f7fa56ef24a48d1269223c
#         http://127.0.0.1:8888/lab?token=2da6189e776bc61c2674a14ef1f7fa56ef24a48d1269223c

## Hit 'ctrl+c' and then 'y' to stop the server.
# Shut down this Jupyter server (y/[n])? y

## Pressing 'Ctrl-C' twice shuts down the Server and immediately destroys the Docker container. 
```