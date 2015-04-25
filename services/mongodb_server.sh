#!/bin/sh

# Mongodb server service
# Usage:
# mongodb_server.sh start/stop/restart

start() {
  mongod --fork --dbpath /data/mongodb/ --logpath /data/log/mongodb/mongodb.log --logappend --port 27018
}
 
stop() {
  mongod --shutdown --dbpath /data/mongodb/
}

case "$1" in
  start)
    start
    ;;
  stop)
    stop   
    ;;
  restart)
    stop
    start
    ;;
  *)
    echo "Usage: mongodb_server.sh {start|stop|restart}"
    exit 1
esac
exit 0
