#!/bin/bash
# Network interface to use
# $1 is the number of iterations to run fping
# $2 is the network interface to use
if [ -z "$1" ]; then
    # fping -c 10 -I bat0 172.27.0.0 172.27.0.1 172.27.0.2 172.27.0.3 172.27.0.4 172.27.0.5 
    fping -c 10 -I $2 172.27.0.0 172.27.0.1 172.27.0.2 172.27.0.3 172.27.0.4 172.27.0.5 
else
#   echo "Running fping for $1 iterations"
    fping -c $1 -I $2 172.27.0.0 172.27.0.1 172.27.0.2 172.27.0.3 172.27.0.4 172.27.0.5 
fi


