FROM python:3.10-alpine3.16
# Install the app
COPY requirements.txt /tmp
RUN mkdir -p /app/data /app/keys /app/fetch /app/present /app/background /app/logs
RUN pip install -r /tmp/requirements.txt
COPY *.py /app
COPY fetch/*.py /app/fetch/
COPY present/*.py /app/present
COPY background/*.py /app/background
# COPY data/* /app/data/
# Install NGINX enable production ready
RUN apk add nginx
COPY nginx/default.conf.http /etc/nginx/http.d/default.conf.http
COPY nginx/default.conf.ssl /etc/nginx/http.d/default.conf.ssl
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY start.sh /app/start.sh
COPY .env /app/.env
RUN chmod +x /app/start.sh
# Set up container connectivity
WORKDIR /app
EXPOSE 80
EXPOSE 443
VOLUME /app/data
VOLUME /app/keys
VOLUME /app/Certs
VOLUME /app/.env
ENTRYPOINT [ "/app/start.sh" ]