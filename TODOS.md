When Deploying:
Change the site domain instead of "example.com" to the actual frontend domain
Change the Registration view to set cookies.

# created test user

> > > test_user = User.objects.create(email="test@gmail.com", password="Panda911")
> > > from allauth.account.models import EmailAddress
> > > EmailAddress.objects.create(user=test_user, email=test_user.email, verified=True)
> > > from job_profile.models import JobDescription
> > > test_jd = JobDescription.objects.create(user=test_user, company_name="Sleep Works", job_position="CEO", job_context="Must be bald and angry")
