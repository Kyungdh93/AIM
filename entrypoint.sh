#!/bin/bash

# Wait for MySQL server to be ready
until netcat -z -v -w30 db 3306; do
  echo "Waiting for MySQL server to be ready..."
  sleep 5
done

# Run FastAPI server
exec "$@"
