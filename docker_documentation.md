RUN DOCKER

# Development

docker compose -f docker-compose.yml -f docker-compose.dev.yml up

# Production (on VM)

docker compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env.prod up -d

THREE STAGE APPROACH

## docker-compose.yml ->

builds 'web', 'nginx' and 'celery' from image and runs entrypoint.sh.
Volumes: static files

## docker-compose.dev.yml ->

builds redis and db containers and connects them.
Volumes: .app codbase and local db data, dev config for nginx

## docker-compose.prod.yml ->

links the .env.prod to celery and web containers. nginx listens on 443
uses independently hosted db and redis
volumes: prod config for nginx, static, ssl certs
