#!/bin/bash

N=$1
if [[ $# -eq 0 ]]
    then
        echo "No arguments supplied. Usage: ./start_sensors <number of processes to start>"
else
    for (( i=1; i<=N; i++ ))
        do
            python3 ./simulator.py ${i} ${N} &
            echo "started simulator with sensor_id=$i"
        done
    echo "done"
fi
