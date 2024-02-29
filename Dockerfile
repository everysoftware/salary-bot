FROM mongo

COPY sample_collection.bson /docker-entrypoint-initdb.d/
COPY sample_collection.metadata.json /docker-entrypoint-initdb.d/

CMD mongod --fork --logpath /var/log/mongodb.log && mongorestore --collection sample_collection --db sampleDB /docker-entrypoint-initdb.d/sample_collection.bson && mongod --shutdown && docker-entrypoint.sh mongod
