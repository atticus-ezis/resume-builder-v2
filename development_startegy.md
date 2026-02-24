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
5. Don't mount volume to current directory for production. You want a replicable, single source of truth. Outside files can override your build-specifics
6. User should be created and given permission to run commands on containers.

Test with
docker compose -f docker-compose-prod.yml --env-file .env.prod up

LEANRED:
Remove app volume mounts in production containers because it will override what is already built.
Create mount volume for static files inside nginx directly so it doens't need to prox request from web.
