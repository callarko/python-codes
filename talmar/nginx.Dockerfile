FROM nginx:stable
COPY nginx.conf /etc/nginx/nginx.conf
COPY server.crt /etc/nginx/certs/server.crt
COPY server.key /etc/nginx/certs/server.key
COPY ca.crt /etc/nginx/certs/ca.crt
