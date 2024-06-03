#!/bin/bash

set -e

host="$1"
port="$2"

until nc -z $host $port; do
  >&2 echo "Kafka is unavailable - sleeping"
  sleep 1
done

>&2 echo "Kafka is up - executing command"
