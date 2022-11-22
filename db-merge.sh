#!/bin/bash

docker-compose stop
sed -i -E 's/DB_MIGRATE=.*/DB_MIGRATE=false/g' .env
docker-compose up -d
./wait-for-it.sh --timeout=120 localhost:4010 -- echo "api is up"
docker-compose exec api flask db merge heads
sed -i -E 's/DB_MIGRATE=.*/DB_MIGRATE=true/g' .env
docker-compose stop
docker-compose up -d
