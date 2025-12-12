App that creates custom Resume's and Cover letters
User to upload their current resume or complete form
Copy and paste the job description
Then download a cover letter or resume tailored to that Job.

Account Creation and Managment -
JWT Cookies that use black list / rotation.
Endpoints come from: Dj Rest Auth
https://github.com/iMerica/dj-rest-auth/
Customized emails to link to frontend.
Created auto-login for email verification and password resets.
Tests:
Ensure custom verify email and confirm password change views return JWT tokens.

Applicant Profile -
Created a "applicant_profile" app that collects personal work history and experience of user.
User can upload Resume PDFs or submit a form to influence the Resume generation.
This info will be saved as UserContext. Each user can have multiple resumes to choose from.

Databases:
context - A single text field used as context for the AI. Will be pdf upload or form.
FK (user) - one-to-many relationship with user.
Form submission strucutre:
[application_context.json](forms/applicant_context.json)

Endpoints (authentication required):
api/context/applicant/ POST - converts pdf to string and returns 200 and text for user review.
{"name", "context"}

"api/applicant/upload-pdf/" POST, DELETE, PUT, PATCH - finalizes the text and saves it to the database returns 200.
{"file"}

creates and saves 201

Job Profile -
Stores context about the job for AI. Frontend will struture the dictionary (hasmap) before sending as "job_context" and "company_name"
if cover letter is selected then additional fields to form will be added such as, (Hiring manager and location)
forms/job_description.json
forms/cover_letter.json

Endpoints (authentication required):
api/context/job/ POST - stores form data with user
{"company_name", "job_context"}

Ai Generation -
Takes context from user and job profiles and passes it to AI. Returns a Mardown text file that can be downloaded as PDF after user-review.
Create 2 prompts with functions - one for resume and cover letter
After initial generation allow a "re-prompt" with user instructions and user edit of mark-down before download.

Databases:
store downloaded version of cover letter + resume
reumse/cover_letter -
FK (user) -
FK (job) -

Endpoints:
generate resume + cover letter:
api/ai-call/ (POST)
{"user_context_id" "job_description_id", "command"}
returns {"response": [{"resume":..}, {"cover letter":...}]}

update prompt:
api/ai-call/update-content/
{"content", "instructions", "content_type": ("resume" or "cover letter")}

download markdown:
api/download-content/
{"markdown_content", "file_name" (build with context: full name)}
returns pdf
