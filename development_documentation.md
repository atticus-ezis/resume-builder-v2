OVERVIEW:

1. Rent a VM
2. Register domain to use VM IP Address
   **Check**
   Frontend now makes a request to domain, traffic routes to VM
3. Use Nginx to proccess request before passing to Django
   **Check**
   Request enters Nginx through 443. Gets matched with a server block where "server_name" matches the domain name being requested. The server block passes to a "proxy" the actual Django code. The "proxy" is [container_name]:[port], example: web:8000. In Docker compose the "web" container is exposed on 8000.
4. In docker-compose Nginx is exposed to incoming traffic from the outside VM via  
   ports:
   - "80:80"
   - "443:443"
5. Create SSL certification in the VM
6. Create a CI/CD pipeline with GitHub Actions that creates a new image when new code is pushed to main, then once the VM is configured add a command that pulls it.

LEARNED:

Remove app volume mounts in production containers because it will override what is already built.
Create mount volume for static files inside nginx directly so it doens't need to prox request from web.
User should be created and given permission in VM to run commands.

THREE STAGE APPROACH:

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

COMMANDS:

# Development

docker compose -f docker-compose.yml -f docker-compose.dev.yml up

# Production (on VM)

docker compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env.prod up -d
