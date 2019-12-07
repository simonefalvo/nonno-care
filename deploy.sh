#!/bin/bash

REGION=$1
BUCKET=$2
if [[ $# -lt 2 ]]
    then
        echo "No arguments supplied. Usage: ./deploy.sh <aws region> <s3 bucket name>"
else
    aws cloudformation package \
        --template-file template.yaml \
        --output-template packaged.yaml \
        --s3-bucket ${BUCKET}

    aws cloudformation deploy \
        --template-file packaged.yaml \
        --region ${REGION} \
        --capabilities CAPABILITY_IAM \
        --stack-name nonno-stack
fi
