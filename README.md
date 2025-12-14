# Resume Builder

App that creates custom resumes and cover letters. Users can upload their current resume or complete a form, copy and paste the job description, then download a cover letter or resume tailored to that job.

## Account Creation and Management

- JWT Cookies that use blacklist / rotation
- Endpoints come from: [Dj Rest Auth](https://github.com/iMerica/dj-rest-auth/)
- urls start with "api/accounts/..."
- Customized emails that link to frontend
- Created auto-login for email verification and password resets

### Tests

Ensure custom verify email and confirm password change views return JWT tokens.

## Applicant Profile

Created an "applicant_profile" app that collects personal work history and experience of user. Users can upload Resume PDFs or submit a form to influence the Resume generation. This info will be saved as UserContext. Each user can have multiple resumes to choose from.

### Databases

- `context` - A single text field used as context for the AI. Will be PDF upload or form.
- FK (user) - one-to-many relationship with user.

### Form Submission Structure

See: [`forms/applicant_context.json`](forms/applicant_context.json)

### Endpoints (authentication required)

- `POST api/context/applicant/upload-pdf` - Converts PDF to string and
  the database, returns 200.

  ```json
  { "file": "...", "name": "..." }
  ```

- `POST/DELETE/PUT/PATCH api/applicant/` - Finalizes the text and saves it to
  returns 200 and text for user review.

  ```json
  { "name": "...", "context": "..." }
  ```

## Job Profile

Stores context about the job for AI. Frontend will structure the dictionary (hashmap) before sending as "job_context" and "company_name". If cover letter is selected then additional fields will be added to form such as Hiring Manager and Location.

See: [`forms/job_description.json`](forms/job_description.json)

### Endpoints (authentication required)

CRUD from viewset

- `POST api/context/job/` - Stores form data with user
- `GET api/context/job/` -
- `GET api/context/job/{id}` -
- `PUT api/context/job/{id}` -
- `PATCH api/context/job/{id}` -
- `DELETE api/context/job/{id}` -
  ```json
  { "company_name": "...", "job_context": "..." }
  ```

## AI Generation

Takes context from user and job profiles and passes it to AI. Returns a Markdown text file that can be downloaded as PDF after user review. Creates 2 prompts with functions - one for resume and cover letter. After initial generation, allows a "re-prompt" with user instructions and user edit of markdown before download.

### Databases

**Note:** Should persist these instances incase user wants to undo future edits.

- Document:
  user (FK)
  user_context (FK)
  job_description (FK)
  document_type: "resume", "cover_letter"
  final_version: DocumentVerison (FK)

- DocumentVersion:
  document (FK)
  markdown: TextField
  version_number: IntField

### Endpoints

#### Generate Resume + Cover Letter

- `POST api/ai-call/`

  ```json
  {
    "user_context_id": "...",
    "job_description_id": "...",
    "command": "generate_resume" | "generate_cover_letter" | "generate_both"
  }
  ```

  Returns:

  ```json
  {
    [
      {
        "markdown": "...",
        "document": { "id": "", "type": "" },
        "document_version": { "id": "", "version": "" }
      }
    ]
  }
  ```

#### Update Prompt

- `POST api/ai-call/update-content/`

  ```json
  {
    "markdown": "optional", // only include if user edits text before re-prompting. This will create a new verssion
    "instructions": "...",
    "document_version_id": "int"
  }
  ```

  Returns:

  ```json
  {
    "markdown": "...",
    "document": { "id": "", "type": "" },
    "document_version": { "id": "", "version": "" }
  }
  ```

#### Download Markdown

Fetch from with saved draft or edited content

- `POST api/finalize-and-download/`
  ```json
  {
    "file_name": "...",
    "document_version_id": "optional",
    "markdown": "optional", // if user edits UI textfield then make this the final version.
    "document_id": "" // needed if version isn't included.
  }
  ```
