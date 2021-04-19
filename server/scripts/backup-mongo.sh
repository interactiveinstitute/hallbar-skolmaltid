# !/bin/sh

DATE=$(date "+%Y%m%d-%H_%M_%S")


# docker exec -it db-mongo mongodump --host localhost --port 27017 -o 
# docker exec -it db-mongo tar -zcvf $current_date.tar.gz dump
# docker cp db-mongo:/$current_date.tar.gz ~/mongodumps/

cd ../docker/


echo "Gonna backup to file: ~/mongodumps/$DATE.dump"
docker-compose exec -T mongo-db sh -c 'mongodump --archive' >  ~/mongodumps/$DATE.dump

echo "Only keep 50 dumps. Removing any older dumps than that"
cd ~/mongodumps/
ls | sort -r | tail -n +51 | xargs rm -v