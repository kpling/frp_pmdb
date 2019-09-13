# Flask RESTPlus PyMongo

Example CRUD app built with Flask, Flask REST Plus, and MongoDB

## Spec
```
Create a Flask microservice with GET, PUT, POST, DELETE endpoints.
Use Flask, Flask-Restplus, PyMongo.

Add text search using jamespath in GET API
Provide filter based upon name and phone number in GET API using jamespath.

As part of POST implementation, Please check validations as written below,

{
    “name”: “string with max limit 64 char”,
    “email”: “string with email format abc@def.com max length 128 char”,
    “phone”: “number 10 digit with + is allowed in first place”,
    “address”: {
        “Address_line_1”: “string max length 256 char”,
        “Address_line_2”: “string max length 256 char”,
        “State”: “string max length 2 char”
        “zip” : “number max lengh”
    }
}


Share your github link with for a quick check

Checklist:
    Flask
        http://flask.palletsprojects.com/en/1.1.x/
    Flask-RESTPlus
        https://flask-restplus.readthedocs.io/en/stable/quickstart.html
    PyMongo
        https://api.mongodb.com/python/current/
    MongoDB
        https://www.mongodb.com/
    GET
        Filtering
            Jamespath
                http://jmespath.org/tutorial.html
    PUT
    POST
        Validation
    DELETE
    Swagger Documentation
        http://editor.swagger.io/
    Github
        https://github.com/kimpeek
    Heroku
        https://dashboard.heroku.com/apps
    Documentation
        markdown
            https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet
```

## TODO
1. Use query strings on url rather than duplicate resources
1. Split app into disparate modules
    1. resources
    1. models
    1. schemas
1. Tests
1. settings config [local, production, testing]
1. mitigate code duplication between model & schema
