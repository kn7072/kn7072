#!/bin/bash
FILE_NAME="cn-aggregated.zone"
# https://www.ipdeny.com/ipblocks/
LINK_CHINA="https://www.ipdeny.com/ipblocks/data/aggregated/${FILE_NAME}"

echo "### BLOCK CHINA ###"
echo "link ${LINK_CHINA}"

ipset -N china hash:net -exist
ipset -F china

if [[ -f "${FILE_NAME}" ]]; then
  rm "${FILE_NAME}"
fi

code=$(wget "${LINK_CHINA}")
if [[ "${code}" -eq 0 ]]; then
  echo "Download finished!"
fi

while IFS= read -r net; do
  ipset -A china "${net}"
done <"${FILE_NAME}"

echo "Done"

echo -n "Blocking CN with iptables..."
iptables -I INPUT -m set --match-set china src -j DROP
echo "Done"
