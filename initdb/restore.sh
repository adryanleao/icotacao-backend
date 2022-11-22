echo "Init databases restore"
mysql -quiet -uroot -p$MYSQL_ROOT_PASSWORD -e 'create database sensi_db_init'

echo "Restoring sensi_db_init"
gunzip < /docker-entrypoint-initdb.d/dumps/sensi_db_init.sql.gz | mysql -quiet -uroot -p$MYSQL_ROOT_PASSWORD sensi_db_init
echo "Databases restore finished ;-)"
