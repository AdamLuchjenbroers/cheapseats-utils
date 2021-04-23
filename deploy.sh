#!/bin/bash

# Simple build and deployment script, since this is too
# basic to warrant its own pipeline yet.

rm -f Package/*

KMS_S3KEY=`aws kms describe-key --key-id alias/aws/s3 --query 'KeyMetadata.KeyId' | tr -d \"`
S3_BUCKET=`aws ssm get-parameter --name "/CheapSeats/Env/ConfigBucket" --query "Parameter.Value" | tr -d \"`
S3_PREFIX=`aws ssm get-parameter --name "/CheapSeats/Env/ConfigBucket/ArtifactPrefix" --query "Parameter.Value" | tr -d \"`

source .config

if [ -z ${STACKNAME+X} ]; then
   echo 'Name of Stack to Deploy?:'
   read STACKNAME

   echo STACKNAME=${STACKNAME} > .config
fi

aws cloudformation package --template-file utils.cf.json --s3-bucket ${S3_BUCKET} --s3-prefix ${S3_PREFIX}/Utils --kms-key-id $KMS_S3KEY --output-template-file Package/utils.cf.json
aws cloudformation deploy --template-file Package/utils.cf.json --stack-name ${STACKNAME} --capabilities CAPABILITY_NAMED_IAM
