#!/bin/bash

aws cloudformation package \
    --template-file template.yaml \
    --output-template packaged.yaml \
    --s3-bucket nonno-care-f

aws cloudformation deploy \
    --template-file packaged.yaml \
    --region eu-central-1 \
    --capabilities CAPABILITY_IAM \
    --stack-name nonno-stack
