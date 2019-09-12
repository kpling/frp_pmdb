# Flask RESTPlus PyMongo

Example CRUD app built with Flask, Flask REST Plus, and MongoDB

## Deployment
```bash
$ heroku create <optional-app-name>
$ heroku git:remote -a <heroku-app-name>
$ heroku addons:create mongolab:sandbox
$ heroku config:set FLASK_ENV=PRODUCTION
$ heroku config:set FLASK_APP=app.py:app
$ heroku config:set FLASK_DEBUG=0
```

## TODO
1. Utilize Flask-PyMongo
1. Deploy