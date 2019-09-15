import os

from flask import Flask
from flask_restplus import Api, Resource
from flask_restplus import fields as model_fields  # workaround for presenting app in one module
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv('MONGODB_URI', "mongodb://localhost:27017/flask_app")

api = Api(app, version='0.1', title='Person API', description='Example CRUD API using a Person model')
ns = api.namespace('person', description='Operations related to people')
mongo = PyMongo(app)

AddressModel = api.model('Address', {
    'line_1': fields.String(max_length=256, example="1234 Main Street"),
    'line_2': fields.String(max_length=256, example="Springfield"),
    'state': fields.String(max_length=2, example="IL"),
    'zip': fields.String(pattern=r'\d{5}', example="12345"),
})

PersonModel = api.model('Person', {
    'name': fields.String(max_length=64, example='John Williams'),
    'email': fields.String(pattern=r'[^@]+@[^@]+\.[^@]+', example='john.williams@email.com'),
    'phone': fields.String(pattern=r'\+?\d{10}', example='1234567890'),
    'address': fields.Nested(AddressModel),
})


@ns.route('/')
class Person(Resource):
    @ns.expect(PersonModel)
    def post(self):
        """Create a person"""

        return {"id": str(document.inserted_id)}


@ns.route('/name/<string:name>')
class PersonNameDetail(Resource):
    def get(self, name):
        """Retrieve a person by name"""


    @ns.expect(PersonModel)
    def put(self, name):
        """Update a person by name"""

        mongo.db.people.update_one({"name": name}, {"$set": person})
        return {'modified': True}
        result = collection.replace_one({"name": name}, api.payload, upsert=False)

    def delete(self, name):
        """Delete a person by name"""

        mongo.db.people.find_one({"name": name})
        return {'deleted': True}


