#!/bin/bash

# sudo apt install jq
# https://jqlang.org/manual/#invoking-jq

function print_info_nodes() {
  for id in $(bspc query --nodes); do
    echo "node id ${id}"
    info_node=$(bspc query --node "${id}" -T)
    # json_info=$(echo $info_node | jq ".id, .client.className, .client.instanceName")
    json_info=$(echo $info_node | jq "pick(.id, .client.className, .client.instanceName)")
    # echo "${json_info}"
    json_filtered=$(echo $json_info | jq "select(.client.className != null)")
    echo "${json_filtered}"
  done
}

print_info_nodes
