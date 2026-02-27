## About this App

This app builds cover letters and tailored resumes for specific job postings in under a minute. Prioritizes speed, ease of use, and customization. I built it to automate copying job descriptions into ChatGPT and manually creating PDFs. This is the backend repo. It handles authentication, AI generation, file downloads and version histories. Frontend repo is here and must be run alongside it: [resume_builder_v2_frontend](https://github.com/atticus-ezis/resume_builder_v2_frontend).

## Design features

**Asynchronous?**  
AI generation requests are handled asynchronously so HTTP requests aren’t blocked while the response is generated. Celery and Redis are used to run this background process.

**Latency?**  
Latency is handled in two ways. (1) User responses are cached and returned instead of triggering an any unnecessary re-generate. (2) Responses are parsed and stored with a `context_hash` that is indexed to avoid caching duplicates by accident.

## How to Run

Choose either Docker or UV

**Docker**
Make sure you have Docker installed and running on your machine first.
https://docs.docker.com/engine/install/

```bash
docker compose -f docker-compose.dev.yml up
```

**UV**
Make sure to install UV on your machine first.
https://docs.astral.sh/uv/getting-started/installation/

```bash
uv sync
source .venv/bin/activate
python manage.py migrate
python manage.py runserver

## in a new tab -

## activate celery
celery -A resume_builder worker -l info --concurrency 1

## create superuser if you want to view the admin panel
python manage.py createsuperuser

```

To view api docs:
http://localhost:8000/api/docs/

To view admin panel:
http://localhost:8000/admin

**_ Docker credentials _**

- username = admin
- password = ThisIsADevelopmentPassword4321!

## Authentication

- JWT in cookies with blacklist and rotation
- Endpoints follow [Dj Rest Auth](https://github.com/iMerica/dj-rest-auth/) under `api/accounts/...`
- includes Gmail backend and password reset and mandatory email verification.

## CI/CD

Uses GitHub Actions to build a Docker image. The image is stored in the repo with the 'latest' tag. On every push to main a new image is built and the image used on the server is updated to build from the 'latest' version. For more details reference the [Deployment Documentation](deployment_documentation.md)

## Tests

Important tests: **Accounts** — full registration and email verification (verify link then login). **AI generation** — duplicate handling (reuse existing document version instead of regenerating; integrity errors for duplicate version name or context hash). **Permissions** — generate endpoint returns 401 when unauthenticated. **Versions** — auto-incrementing and custom version names for document versions.
