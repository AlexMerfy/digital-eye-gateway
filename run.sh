#!/usr/bin/with-contenv bashio
set -e

bashio::log.info "Digital Eye Gateway started."
exec gunicorn \
  --bind 0.0.0.0:8099 \
  --workers 1 \
  --threads 4 \
  --timeout 60 \
  --access-logfile - \
  --error-logfile - \
  gateway:app
