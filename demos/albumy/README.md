### chores

1. admin email: `a1211071880@163.com`, password: `admin@520`


### TEST UI NOTES

1. activate virtual env by pipenv

  ```
  pipenv shell
  ```

2. run test app server:

  ```
  set FLASK_APP=test_app.py & flask run
  ```

3. run test case:

  ```
  python-m unittest tests.test_ui
  ```

4. coverage test

  ```
  coverage run -m unittest discover
  ```

  > need to install coverage before by ```pipenv install coverage --dev```

5. preview coverage report

  ```
  coverage html
  ```

### CHECK CODE QUALITY

1. intall flake8 by pipenv

  ```
  pipenv install flake8 --dev
  ```

2. check

  ```
  flake8 [package name]
  ```