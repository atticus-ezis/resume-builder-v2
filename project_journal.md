2/20/26
Test celery call in local.
Check network response on frontend.
Test Docker using compose and then Dockerfile with commands
Update redis to use new commands and .envs
{
REDIS_HOST

}
Update vercel
Test production

PROBLEM:
In production:

1. task runs indefintley
   In development
2. Web container lacks permission

SOLUTIONS:

1. run celery next time
