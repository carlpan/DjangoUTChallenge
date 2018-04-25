# Instructions

### Getting started

1. Go to this [link](https://www.dropbox.com/sh/o2fpjaj4fjp7wqa/AAD9gR9-0NcKpZxvDupFtHEHa?dl=0) to download db.sqlite3 and copy and paste it into the root directory.
2. Initialize a virtual environment by running `virtualenv env`. If it succeeds, proceed to step 5.
3. Install pip with `curl -O https://bootstrap.pypa.io/get-pip.py` `sudo python get-pip.py`.
4. Install virtualenv with `sudo pip install virtualenv`.
5. `source env/bin/activate`
7. `pip install -r requirements.txt`
8. Create an admin user by typing `python manage.py createsuperuser` in the root directory.
9. `./manage.py migrate`
10. `./manage.py collectstatic`
11. `./manage.py runserver`

### Next step

Now you can proceed to the browser and check the following urls:
1. http://127.0.0.1:8000/amdin
2. http://127.0.0.1:8000/call_schedules

The first url is where you can locate all the existing models in the apps and the second url gives an example flow for api_1 app. Please read further instructions in each app to find more details.

IMPORTANT: please go to 'test' folder in each app ('api_1' and 'api_2') to complete writing unit tests.

### How to run test

You can test each test case after writing it by tying the following:
```
py.test path/to/test.py -k 'test_method_name'
```

Refer to Django's official reference page for testing [here](https://docs.djangoproject.com/en/2.0/topics/testing/).
You can learn more about pytest [here](https://docs.pytest.org/en/latest/).

### How to run coverage

You can check code test coverage by typing the following:
```
py.test --cov-config .coveragerc --cov ./
```
You can learn more about code coverage [here](https://pypi.org/project/pytest-cov/).
