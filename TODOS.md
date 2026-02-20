AI OPTIMIZATION ######## 2. add redis and celery 3. rate-limiting per user 4. consider batching (one call for resume and cover letter generation) 5. add instructions to versions for logging

REDIS ->
add Docker command that starts and runs redis. Add redis to docker-compose
docker run -d -p 6379:6379 redis

Add this instruction to README.MD startup
cd /Users/atticusezis/coding/resume_builder_v2
celery -A resume_builder worker -l info

!!!! IMPORTAMT MUST ADD START COMMAND 'web' and 'celery' IN REDIS
