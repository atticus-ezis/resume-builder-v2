2/20/26
PROBLEM:
In production:

1. task runs indefintley in development
2. Web container lacks permission
3. Production server is stalling when I login with Google
   My cors rejects the google/ call and I get a 500 error

﻿

SOLUTIONS:

1. run celery next time
2. (and 3) csrf allowed origins needed to be set

2/24/26
PROBLEM:
Failing health check. Response isn't rendering.
'''
resume-builder-web | AssertionError: .accepted_renderer not set on Response
dependency failed to start: container resume-builder-web is unhealthy
'''
The health-check is failing because the Response isn't rendering.
SOLUTION:
Use HttpResponse instead of Response.
Rebuilt the docker-compose to use the fixed code.
PROBLEM:
ssl certification failed
'''
resume-builder-nginx | 2026/02/24 05:37:41 [emerg] 1#1: cannot load certificate "/etc/nginx/certs/fullchain.pem": PEM_read_bio_X509_AUX() failed (SSL: error:0480006C:PEM routines::no start line:Expecting: TRUSTED CERTIFICATE)
'''
SOLUTION
ssl certification happens in the VM.
