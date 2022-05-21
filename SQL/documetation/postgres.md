docker run --name habr-pg-14.3 -p 5555:5432 -e POSTGRES_USER=habrpguser -e POSTGRES_PASSWORD=pgpwd4habr -e POSTGRES_DB=habrdb -d --rm postgres:14.3
psql -h localhost -p 5555 -U habrpguser -d habrdb


psql -h 127.0.0.1 -p 5555 -U postgres


docker run --rm -P -p 127.0.0.1:5555:5432 -e POSTGRES_PASSWORD="1234" --name pg postgres:14.3
psql postgresql://postgres:1234@localhost:5555/postgres


psql -h localhost -p 5416 -U <my-user> -d <my-database>

psql -h localhost -p 5555 -U habrpguser -d habrdb