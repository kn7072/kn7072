## запуск контейнера с базой habrdb
[ссылка на примеры](https://habr.com/ru/post/578744/?ysclid=l3bvdxf8nh)
docker run --name habr-pg-14.3 -p 5555:5432 -e POSTGRES_USER=user -e POSTGRES_PASSWORD=123 -e POSTGRES_DB=habrdb -d --rm postgres:14.3

----

docker run --name habr-pg-14.3 -p 5555:5432 -e POSTGRES_USER=user -e POSTGRES_PASSWORD=123 -d -v "/home/stapan/sql/base_init":/docker-entrypoint-initdb.d postgres:14.3

psql -h localhost -p 5555 -U user
----
1. __Для первого запуска__

    docker run --name habr-pg-14.3 -p 5555:5432 -e PGDATA=/var/lib/postgresql/data/pgdata -e POSTGRES_USER=user -e POSTGRES_PASSWORD=123 -d -v "/home/stapan/sql/base_init":/docker-entrypoint-initdb.d -v "/home/stapan/sql/base":/var/lib/postgresql/data postgres:14.3

2. __Удаляем контейнер__

    docker rm -f <container_id>

3. __Запускаем контейнер__

    docker run --name habr-pg-14.3 -p 5555:5432 -e PGDATA=/var/lib/postgresql/data/pgdata -e POSTGRES_USER=user -e POSTGRES_PASSWORD=123 -d -v "/home/stapan/sql/base":/var/lib/postgresql/data postgres:14.3
   
----

docker run --name habr-pg-14.3 -p 5555:5432 -e POSTGRES_USER=user -e POSTGRES_PASSWORD=123 -e POSTGRES_DB=habrdb -d --rm -v "/home/stapan/sql/base":/docker-entrypoint-initdb.d postgres:14.3

psql -h localhost -p 5555 -U habrpguser -d habrdb


psql -h 127.0.0.1 -p 5555 -U postgres


docker run --rm -P -p 127.0.0.1:5555:5432 -e POSTGRES_PASSWORD="1234" --name pg postgres:14.3
psql postgresql://postgres:1234@localhost:5555/postgres


psql -h localhost -p 5416 -U <my-user> -d <my-database>

psql -h localhost -p 5555 -U habrpguser -d habrdb