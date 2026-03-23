#!/bin/bash

FILE="bad_hosts.txt"

ipset -N bad_hosts iphash -exist
ipset -F bad_hosts

echo "Adding IPs from file to bad_hosts"

while IFS= read -r ip; do
  ipset -A bad_hosts "${ip}"
  echo -n "${ip}|"
done <"${FILE}"

echo -e -n "\nDropping with iptables..."

iptables -I INPUT -m set --match-set bad_hosts src -j DROP
echo "Done"
# ipset -L bad_hosts
