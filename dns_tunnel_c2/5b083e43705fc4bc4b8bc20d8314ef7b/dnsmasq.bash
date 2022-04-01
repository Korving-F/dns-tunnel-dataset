#!/bin/env bash
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y dnsmasq

DNS_SERVER="192.168.0.20"
cat << EOF > /etc/dnsmasq.conf
log-queries
log-facility=/var/log/dnsmasq.log
no-resolv
server=9.9.9.9
server=8.8.8.8
server=/attack/$DNS_SERVER
strict-order
EOF
