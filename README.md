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
/upload/pdf/ POST - converts pdf to string and returns 200 and text for user review.

"api/applicant/user-context/" POST, DELETE, PUT, PATCH - finalizes the text and saves it to the database returns 200.

Job Application -
Stores context about the job for AI. Frontend will struture the dictionary (hasmap) before sending as "job_context" and "company_name"
if cover letter is selected then additional fields to form will be added such as, (Hiring manager and location)
forms/job_description.json
forms/cover_letter.json

Endpoints (authentication required):
/job-description/ POST - stores form data with user
send ("job_context" and "company_name")
