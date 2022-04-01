#!/bin/env bash
echo "Installing IODINE"
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y git make build-essential pkg-config zlib1g-dev net-tools openssh-server iputils-ping netcat dnsutils libtext-lorem-perl sshpass asciinema
cd /opt
git clone https://github.com/yarrick/iodine.git
cd /opt/iodine
make
make install