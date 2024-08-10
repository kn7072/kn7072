#!/bin/bash

set -x
# список сигналов можно узнать вызвав в терминале trap -l
trap 'docker container stop $container_id; exit' INT TERM

container_id=$(docker run --rm --name pg -p 5432:5432 -e POSTGRES_USER=user -e POSTGRES_PASSWORD=123 -e PGDATA=/var/lib/postgresql/data/pgdata -d -v "/home/stepan/sql/data":/var/lib/postgresql/data postgres)
echo $container_id
sleep 24h
