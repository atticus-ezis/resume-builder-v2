## About this App

This app builds cover letters and tailored resumes for specific job postings in under a minute. Prioritizes speed, ease of use, and control. I built it to automate copying job descriptions into ChatGPT and manually creating PDFs. This is the backend. It handles authentication, AI generation, pdf downloads and version histories. API docs are at available at `/api/docs`. Frontend repo is here: [resume_builder_v2_frontend](https://github.com/atticus-ezis/resume_builder_v2_frontend).

## Design features

**Asynchronous?**  
AI generation requests are handled asynchronously so HTTP requests aren’t blocked while the response is generated. Celery and Redis are used to run this background process.

**Latency?**  
Latency is handled in two ways. (1) User responses are cached and returned instead of triggering an any unnecessary re-generate. (2) Responses are parsed and stored with a `context_hash` that is indexed to avoid caching duplicates by accident.

## How to Run

**Docker**

```bash
docker compose -f docker-compose.dev.yml up
```

Then open: http://localhost:8000/api/docs/

**UV**

```bash
uv sync
source .venv/bin/activate
python manage.py migrate
python manage.py runserver
```

Then open: http://localhost:8000/api/docs/

## Authentication

- JWT in cookies with blacklist and rotation
- Endpoints follow [Dj Rest Auth](https://github.com/iMerica/dj-rest-auth/) under `api/accounts/...`
- Custom emails with links to the frontend; auto-login after email verification and password reset

## CI/CD

Uses GitHub Actions to build a Docker image. The image is stored in the repo with the 'latest' tag. On every push to main a new image is built and the image used on the server is updated to build the 'latest' version. For more details reference the [Deployment Documentation](deployment_documentation.md)

## Tests

Important tests: **Accounts** — full registration and email verification (verify link then login). **AI generation** — duplicate handling (reuse existing document version instead of regenerating; integrity errors for duplicate version name or context hash). **Permissions** — generate endpoint returns 401 when unauthenticated. **Versions** — auto-incrementing and custom version names for document versions.
