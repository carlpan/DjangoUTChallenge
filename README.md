# Instructions

### Getting started

1. Go to this link to download db.sqlite3 and copy and paste it into the root directory.
2. Initialize a virtual environment by running `virtualenv env`. If it succeeds, proceed to step 5.
3. Install virtualenv with pip if you don't already have it.
4. Install pip if you don't already have it.
5. `source env/bin/activate`
6. Create an admin user by typing `python manage.py createsuperuser` in the root directory.
7. `./manage.py migrate`
8. `./manage.py collectstatic`
9. `./manage.py runserver`

Now you can proceed to the browser and check the following urls:
1. http://127.0.0.1:8000/amdin
2. http://127.0.0.1:8000/call_schedules
The first url is where you can locate all the existing models in the apps and the second url gives an example flow for api_1 app.

Please read further instructions in each app to find more details.
