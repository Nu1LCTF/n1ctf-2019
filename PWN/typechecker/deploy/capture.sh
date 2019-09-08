#!/bin/bash

umask 0077
cd "$(dirname ${BASH_SOURCE[0]})/pcap/"
tcpdump -G 600 -i eth0 -w ./chaldump-%Y-%m-%d_%H-%M-%S.pcap 'port 9999'

