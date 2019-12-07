#!/bin/bash

REGION=$1
if [[ $# -eq 0 ]]
    then
        echo "No arguments supplied. Usage: ./describe_stack.sh <aws region>"
else
    aws cloudformation describe-stacks \
        --stack-name nonno-stack \
        --region ${REGION} \
        --query "Stacks[].Outputs"
fi
