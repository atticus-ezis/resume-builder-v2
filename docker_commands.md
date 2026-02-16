CHECK:
docker ps

FOR COMPOSE-FILE:
docker-compose.yaml

FOR DOCKER IMAGE:
docker build -t ats-resume-builder .
docker run -p 8000:8000 ats-resume-builder

STOP:
docker stop {CONTAINER ID}

DOCKER HUB:
docker build -t ats-resume-builder:v1 .
docker tag ats-resume-builder:v1 yourusername/ats-resume-builder:v1
docker push yourusername/ats-resume-builder:v1
