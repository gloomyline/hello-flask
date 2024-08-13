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