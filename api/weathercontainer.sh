#!/bin/bash

# docker run -d -p5001:443 --restart=always \
docker run -d -p5001:5001 --restart=always \
-v ./Data:/app/Data -v ./Keys:/app/Keys \
--name=weatherservice \
steve353/weatherapi:3.0
# -v ./Certs:/app/Certs \
