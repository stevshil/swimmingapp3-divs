#!/bin/bash

# Old version
# docker run -d -p5001:5001 --restart=always \
# -v ./Data:/app/data -v ./Keys:/app/keys \
# - v ./.env:/app/.env \
# --name=weatherservice \
# steve353/weatherapi:v2-1.0

cd ${HOME}/weather
docker-compose up -d