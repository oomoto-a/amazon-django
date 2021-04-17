array=(`docker ps | grep 0.0.0.0:3306`)
docker exec $array mysqldump -u root --password=docker docker | gzip > dump.sql.gz
pause
