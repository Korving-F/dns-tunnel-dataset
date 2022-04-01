#!/bin/env bash
echo "Installing IODINE"
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y git make build-essential pkg-config zlib1g-dev net-tools openssh-server iputils-ping netcat dnsutils libtext-lorem-perl sshpass asciinema
cd /opt
git clone https://github.com/yarrick/iodine.git
cd /opt/iodine
make
make install

echo "Setup SSH Daemon"
mkdir -p /var/run/sshd
echo "root:root" | chpasswd
sed -ri "s/^#?PermitRootLogin\s+.*/PermitRootLogin yes/" /etc/ssh/sshd_config
sed -ri "s/UsePAM yes/#UsePAM yes/g" /etc/ssh/sshd_config; sed -ri "s/PasswordAuthentication no/PasswordAuthentication yes/g" /etc/ssh/sshd_config
mkdir /root/.ssh

echo "Setting up testfile"
cd /root
lorem -p 10000 > test-file