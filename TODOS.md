group cover letter + resume as single application

check by running the docker gunicorn service and see if frontend can connect.

Important Checks:
make sure the same generation doesn't occur twice. If the combination of job and application exist, search for an existing document before regenerating.

When Deploying:
Change the site domain instead of "example.com" to the actual frontend domain

To Optimize:
Figure out a way to make the homepage load quicker. Add redis. Consider submitting and saving one large request instead of three. Compare results.

when generating new. The history must be updated

# created test user

> > > test_user = User.objects.create(email="test@gmail.com", password="Panda911")
> > > from allauth.account.models import EmailAddress
> > > EmailAddress.objects.create(user=test_user, email=test_user.email, verified=True)
> > > from job_profile.models import JobDescription
> > > test_jd = JobDescription.objects.create(user=test_user, company_name="Sleep Works", job_position="CEO", job_context="Must be bald and angry")

"email": "test@gmail.com",
"email_verified": false,

is this true?
