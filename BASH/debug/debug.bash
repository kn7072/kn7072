#!/bin/bash

# https://blog.site-home.ru/pipefail.html
set -euxo pipefail

trap 'echo "# $BASH_COMMAND";read' DEBUG

echo line1
echo line2
echo line3

