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
User can upload multiple different Resume PDFs or submit multiple forms to influence the Resume generation.
Can be stored with names.

Databases:
resume_data - A single raw JSON field used as context for the AI. FK (user) one-to-many relationship with user.
Form submission strucutre:
[form.json](form.json)

Endpoints (authentication required):
/upload/pdf/ POST - converts pdf to string and returns 200 and texxt for user review.

confirm/context/ POST - finalizes the text and saves it to the database returns 200.
