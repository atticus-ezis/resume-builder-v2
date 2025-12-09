# confirm email -

use a custom adapter to set the frontend as the reset url
write a custom view that accepts the key as a post request and validates email
return either a success or auto-login

# reset password -

email link points to frontend
frontend sends new pass + keys to the default backend
when creafting email, use adapter or custom template
might need name="password_reset_confirm", as placeholder

rmc used -
serializer --> specified form.py
form.py created context variables and sent template w/ context via adapter

# reset password -

custom adapter that points to frontend
custom view that accepts key + uid

#1 Install deps and configure settings
DRF, JWT, dj-rest-auth
add jwt settings, rotation, all auth behavior
#2 Create account app and wire account creation and mgmt
login, register, verify, reset, etc...
create user profile model with FK to user.
#3 connect the api to chatgpt

http://localhost:3000/users/password/reset?token=3Dd0frrh-ce11fa42a7a5f39342c=
94d5d65d85686&uid=3Du

token = d0frrh-ce11fa42a7a5f39342c94d5d65d85686
uid=u
