#!/bin/sh

# Simple build and deployment script, since this is too
# basic to warrant its own pipeline yet.

rm -f Package/*

KMS_S3KEY=`aws kms describe-key --key-id alias/aws/s3 --query 'KeyMetadata.KeyId' | tr -d \"`

aws cloudformation package --template-file utils.cf.json --s3-bucket deimos-configmgmt --s3-prefix Build/Artifacts/Urila --kms-key-id $KMS_S3KEY --output-template-file Package/utils.cf.json
aws cloudformation deploy --template-file Package/utils.cf.json --stack-name deimos-utils --capabilities CAPABILITY_NAMED_IAM
