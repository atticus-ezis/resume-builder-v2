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
context - A single text field used as context for the AI. Will be pdf text or form.
FK (user) - one-to-many relationship with user.
Form submission strucutre:
[application_context.json](forms/applicant_context.json)

Endpoints (authentication required):
api/context/applicant/ POST - converts pdf to string and returns 200 and text for user review.

"api/applicant/upload-pdf/" POST, DELETE, PUT, PATCH - finalizes the text and saves it to the database returns 200.

Job Profile -
Stores context about the job for AI. Frontend will struture the dictionary (hasmap) before sending as "job_context" and "company_name"
if cover letter is selected then additional fields to form will be added such as, (Hiring manager and location)
forms/job_description.json
forms/cover_letter.json

Endpoints (authentication required):
api/context/applicant/ POST - stores form data with user
send ("job_context" and "company_name")

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
generate resume -
generate cover letter -
update resume -
update cover letter -
download resume -
download cover letter -

Functions:
Generate AI prompts for cover letter + resume. - Content must be strictly .md so it's ready to download - Must reject "AI Detection prompts" - Must not use "[placeholders]"

Download md to pdf
