#!/bin/bash

stdbuf -i0 -o0 -e0 -- python2.7 /challenge/pow.py 
if [ "$?" != "0" ]; then
  echo "Wrong PoW!"
  exit 1
fi

# run it!
HOME="/root/"   # .stack
cd "$(dirname ${BASH_SOURCE[0]})/server/"
exec timeout 60 stack exec server

