#!/bin/bash
datadir=~/.dataDir
mkdir -p ~/.aws
cp config ~/.aws
aws sso login --no-browser
mkdir -p ${datadir}
aws s3 sync s3://securiti-state-718391394098/cx/ ${datadir}
start-notebook.sh --allow-root