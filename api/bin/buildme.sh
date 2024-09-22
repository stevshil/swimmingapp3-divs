#!/usr/bin/env bash

if (( $# < 1 ))
then
    echo "SYNTAX: $0 <version>" 1>&2
    exit 1
fi

version=$1
docker build -t steve353/weatherapi:${version} .