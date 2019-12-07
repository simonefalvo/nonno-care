#!/bin/bash

BUCKET=$1
if [[ $# -eq 0 ]]
    then
        echo "No arguments supplied. Usage: ./train_model <s3 bucket name>"
else
    cd ./ml_training/
    python3 ./remove_role.py
    python3 ./train_python.py ${BUCKET}
    cd ..
fi