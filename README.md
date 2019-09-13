# Flask RESTPlus PyMongo

Example CRUD app built with Flask, Flask REST Plus, and MongoDB

## Spec
* [X] Create a Flask microservice with GET, PUT, POST, DELETE endpoints.
* [X] Use Flask, Flask-Restplus, PyMongo.

* [ ] Add text search using jamespath in GET API
* [ ] Provide filter based upon name and phone number in GET API using jamespath.

* [X] As part of POST implementation, Please check validations as written below,
```
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
```
