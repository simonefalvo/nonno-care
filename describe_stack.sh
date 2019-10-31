#!/bin/bash

aws cloudformation describe-stacks --stack-name nonno-stack --region eu-west-3 \
    --query "Stacks[].Outputs"
