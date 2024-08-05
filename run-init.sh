#!/bin/bash
if [ -z "${SYNC_S3}" ]
then
    echo "Skipping s3 authentication and sync".
else
    datadir=~/.dataDir
    mkdir -p ~/.aws
    cp config ~/.aws
    aws sso login --no-browser
    rm -rf ${datadir}
    mkdir -p ${datadir}
    s3fetch s3://securiti-cx-exports/cx/ --download-dir ${datadir} --threads 100
fi
echo "Setting password for jupyter server to 'my-password'"
start-notebook.py --allow-root --PasswordIdentityProvider.hashed_password='argon2:$argon2id$v=19$m=10240,t=10,p=8$JdAN3fe9J45NvK/EPuGCvA$O/tbxglbwRpOFuBNTYrymAEH6370Q2z+eS1eF4GM6Do'
