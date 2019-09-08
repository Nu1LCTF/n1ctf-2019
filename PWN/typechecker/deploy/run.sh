#!/bin/bash

HOME="/root/" # .stack
cd `dirname ${BASH_SOURCE[0]}`
exec python2.7 server.py

