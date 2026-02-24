## About this App

This is an app that lets you build custom cover-letters and resumes in less than a minute. Why? I found myself copy and pasting job descriptions along with my resume into chatGPT and creating new pdf files from Google docs for every application. If you apply to 5 + roles a day that can be very fatiguing, so I built this app to streamline the process and save time. AI is being used to screen resumes and cover-letters (ATS) so you migth as well use AI tools to your advantage.

This is the backend for the app. It manages user Authentication, and database requests.
You can refrence the API endpoints (documented clearly at /api/docs) to make these requests.
The frontend repo can be found here: https://github.com/atticus-ezis/resume_builder_v2_frontend

## Custom Logic

**Backend Best Practices** Filter all documents by user and enforce permissions. Index custom fields like content_hashmap to speed up lookups. Enforce integrety errors to prevent duplicate content. Verify requests, handle error messages, create tests for custom logic and enpoint behavior.

**Speed and efficiency:** Resumes can be uploaded as PDFs and reused across applications. A single endpoint generates both the resume and cover letter in one request. To avoid duplicate work, the system checks for an existing version before regenerating; if a match is found, it returns that version immediately. Users can force regeneration when content is corrupted or outdated. Markdown content is hashed for fast lookup and to prevent duplicate versions with identical content or names.

**Customizability:** Resumes and cover letters are fully editable. Version history is preserved so users can track changes over time. Users can re-prompt the AI to refine suggestions or fix errors that are difficult to correct manually. These instructions are injected directly into the AI prompt, and the updated content is regenerated and saved as a new version.

## How to Run?

With Docker or with UV

1. Docker:

- Install and run docker locally.
- Navigate to root directory (with docker-compose.yaml file)
- Run the following command

```
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```

- visit:
  http://0.0.0.0:8000/api/docs/

2. UV:

- Install UV (package manager) locally
- Navigate to root directory
- Run the commands

```
uv sync

source .venv/bin/activate

python manage.py migrate

python manage.py runserver

```

- visit:
  http://127.0.0.1:8000/api/docs/

## Account Creation and Management

- JWT Cookies that use blacklist / rotation
- Endpoints come from: [Dj Rest Auth](https://github.com/iMerica/dj-rest-auth/)
- urls start with "api/accounts/..."
- Customized emails that link to frontend
- Created auto-login for email verification and password resets

### Tests

Ensure custom verify email and confirm password change views return JWT tokens.
