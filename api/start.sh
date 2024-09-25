#!/bin/sh

if [[ -e /app/Certs/fullchain.pem ]]
then
    cp /etc/nginx/http.d/default.conf.ssl /etc/nginx/http.d/default.conf
else
    cp /etc/nginx/http.d/default.conf.http /etc/nginx/http.d/default.conf
fi
(
nginx
python apiserver.py 
)>/dev/stdout 2>/dev/stderr