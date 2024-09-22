#!/usr/bin/env bash

if (( $# < 1 ))
then
    echo "SYNTAX: $0 <version>" 1>&2
    exit 1
fi

version=$1

docker run -d -p5001:443 --restart=always -v ${PWD}/Data:/app/Data \
    -v ${PWD}/Keys:/app/Keys -v ${PWD}/Certs:/app/Certs  \
    --name=weatherservice steve353/weatherapi:${version}