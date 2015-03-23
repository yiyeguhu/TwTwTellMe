#!/bin/sh

service() {
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
}
