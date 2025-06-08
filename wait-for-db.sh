#!/bin/sh
# wait-for-db.sh

set -e
  
host="$1"
shift
cmd="$@"
  
until mysqladmin ping -h "$host" -u "username" -p"password" --silent; do
  >&2 echo "MySQL is unavailable - esperando..."
  sleep 2
done
  
>&2 echo "MySQL está listo - ejecutando comando"
exec $cmd
