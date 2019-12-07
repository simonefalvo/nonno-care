#!/bin/bash

EMAIL=$1
if [[ $# -eq 0 ]]
    then
        echo "No arguments supplied. Usage: ./verify_email.sh <receiver@example.com>"
else
    aws ses verify-email-identity --email-address ${EMAIL}
fi
