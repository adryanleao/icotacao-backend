#!/bin/bash

docker-compose exec -T mysql mysqldump -uroot -proot sensi_db_init > initdb/dumps/sensi_db_init.sql
cd initdb/dumps
gzip -f sensi_db_init.sql
