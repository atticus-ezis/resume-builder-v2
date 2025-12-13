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
  { "file": "..." }
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

- `POST api/context/job/` - Stores form data with user
  ```json
  { "company_name": "...", "job_context": "..." }
  ```

## AI Generation

Takes context from user and job profiles and passes it to AI. Returns a Markdown text file that can be downloaded as PDF after user review. Creates 2 prompts with functions - one for resume and cover letter. After initial generation, allows a "re-prompt" with user instructions and user edit of markdown before download.

**Note:** All generated and updated content is automatically saved as drafts to the database, allowing users to resume work later.

### Databases

- `resume/cover_letter` - Stores draft and final versions of cover letter + resume
- FK (user) - one-to-many relationship with user
- FK (job) - one-to-many relationship with job

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
    "markdown": [{ "resume": "..." }, { "cover letter": "..." }]
  }
  ```
  **Note:** Automatically saves generated content as drafts to the database.

#### Update Prompt

- `POST api/ai-call/update-content/`
  ```json
  {
    "content": "...",
    "instructions": "...",
    "content_type": "resume" | "cover letter",
    "job_description_id": "..."
  }
  ```
  Returns:
  ```json
  {
    "markdown": "..."
  }
  ```
  **Note:** Automatically saves updated content as a draft to the database.

#### Download Markdown

- `POST api/download-content/`

  Option A: Fetch from saved draft (recommended)

  ```json
  {
    "file_name": "...",
    "job_description_id": "...",
    "content_type": "resume" | "cover letter"
  }
  ```

  Option B: Override with edited content

  ```json
  {
    "markdown_content": "...",
    "file_name": "...",
    "job_description_id": "...",
    "content_type": "resume" | "cover letter"
  }
  ```

  Returns: PDF file (also saves final version to database)

  **Note:** If `markdown_content` is not provided, the endpoint fetches the latest saved draft from the database. If provided, it uses that content (allowing for local edits) and saves it as the final version.
