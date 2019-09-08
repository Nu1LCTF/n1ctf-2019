#!/bin/sh

# install dependencies
apt install -y tcpdump

# make shared directory
mkdir /files/

# setup cron job
cp ./deploy/cron.sh /root/
chmod +x /root/cron.sh
echo "*/5 * * * * /root/cron.sh" | crontab -

# make flag_reader
make

# setup traffic capture
mkdir /root/pcap/
cp ./deploy/capture.sh /root/ && chmod +x /root/capture.sh
pushd .
cd /root/
nohup ./capture.sh & > /dev/null
popd

