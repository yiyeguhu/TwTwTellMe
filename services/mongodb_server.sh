#!/bin/bash

# Mongodb server service
# Usage:
# mongodb_server.sh start/stop/restart

source service.sh

start() {
  mongod --fork --dbpath /data/mongodb/ --logpath /var/log/mongodb.log
}
 
stop() {
  mongod --shutdown --dbpath /data/mongodb/
}

service $1
