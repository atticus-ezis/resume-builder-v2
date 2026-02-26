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

TWO FILE APPROACH:

## docker-compose.dev.yml ->

Builds web, celery, nginx from Dockerfile. Runs db and redis locally.
Volumes: app codebase, local db data, dev nginx config.

## docker-compose.prod.yml ->

Pulls web and celery from GHCR image. nginx listens on 443.
Uses independently hosted db and redis.
Volumes: prod nginx config, static files, SSL certs.

COMMANDS:

# Development

docker compose -f docker-compose.dev.yml up

# view logs:

docker compose -f docker-compose.dev.yml logs

# down and remove volumes

docker compose -f docker-compose.dev.yml down -v

# build

docker compose -f docker-compose.dev.yml up --build

# Production (on VM)

docker compose -f docker-compose.prod.yml up -d --pull always
