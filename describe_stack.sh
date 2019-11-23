#!/bin/bash

aws cloudformation describe-stacks \
    --stack-name nonno-stack \
    --region eu-central-1 \
    --query "Stacks[].Outputs"
