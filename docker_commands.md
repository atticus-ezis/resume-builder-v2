CHECK:
docker ps

FOR COMPOSE-FILE:
docker-compose.yaml

FOR DOCKER IMAGE:
docker build -t ats-resume-builder .
docker run -p 8000:8000 ats-resume-builder

STOP:
docker stop {CONTAINER ID}
