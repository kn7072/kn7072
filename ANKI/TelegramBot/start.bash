#!/bin/bash

set -p
python sound_word.py &

echo "PID родительского процесса $$"
echo "PID sound_word.py $!"
SOUND_WORD_PID=$!

python server.py &
echo "PID server.py $!"
SERVER_PID=$!

trap "kill -SIGTERM $SOUND_WORD_PID $SERVER_PID" SIGINT SIGTERM
wait