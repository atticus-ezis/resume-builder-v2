Try running celery service in the same Dockerfile as 'web' service for Render.
DECIDE ON HOSTING
Provider on Render or VPS

Create a docker-compose with nginx
Research deployment and hosting on Hertz VM.

DEPLOY TO VPS (Eventually)
Create a CI/CD Pipleine with GitHub Actions that triggers on push to main.
Automatically build image, push and pull in server with ssh and restart server

On your VM, before starting the containers, get a cert with certbot:
sudo apt install certbot
sudo certbot certonly --standalone -d your-domain.com

Link The Official site email
