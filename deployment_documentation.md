OVERVIEW:

1. Domain has a DNS record that is proxied through cloudflare and passed to server's IPv4 address (hosted on ionos)
2. The server uses Caddy as a reverse proxy

- Caddy gets its own directory: /opt/caddy/
- Inside is /opt/caddy/Caddyfile, & /opt/caddy/compose.yml
- Compose.yml stores volumes for SSL certs, and references the Caddyfile.
- Exposes ports (443, 80)
- Connects to 'shared-network' for other containers to use.
- Caddyfile points the api.ats-resume-builder.com host to the correct web:8000 container and stores logs in caddy's volume.

3. App runs as a seperate Docker container in server

- Copied "docker-compose.prod" to /opt/resume-builder/compose.yml on the server
- Added .evn.prod to /opt/resume-builder/.env.prod
- The compose.yml connects to "shared-network" so it's discoverable by "caddy"
- The image the compose.yml builds from is a GitHub stored image that is up-to-date with "main" branch.
- The entrypoint.sh used accepts commands ['web'] and ['celery'] that starts gunicorn or celery worker using the same build image.
- The DB and Redis host are external services referenced in the image as urls.

EXECUTE:

- Inside VM...
- cd /opt/caddy/: run: docker compose up -d
- cd /opt/resume-builder/: docker compose pull, docker compose up -d

DEVELOPMENT COMMANDS:

# Development

docker compose -f docker-compose.dev.yml up

# view logs:

docker compose -f docker-compose.dev.yml logs

# down and remove volumes

docker compose -f docker-compose.dev.yml down -v

# build

docker compose -f docker-compose.dev.yml up --build
