#!/bin/bash

N=$1
SENSORS=500
if [[ $# -eq 0 ]]
    then
        echo "No arguments supplied. Usage: ./start_sensors <number of processes to start>"
else
    cd ./wirlband_simulator/
    for (( i=0; i<N; i++ ))
        do
            python3 ./simulator.py ${SENSORS} ${i} &
            echo "started simulator $i of $SENSORS users"
        done
    echo "done"
    cd ..
fi
