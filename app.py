import os

from flask import Flask
from flask_restplus import Api, Resource, fields
from pymongo import MongoClient

app = Flask(__name__)
MONGO_URI = os.getenv('MONGODB_URI', "mongodb://localhost:27017")

api = Api(app, version='0.1', title='Person API', description='Example CRUD API using a Person model', validate=True)
ns = api.namespace('person', description='Operations related to people')
collection = MongoClient(MONGO_URI).flask_app.person

AddressModel = api.model('Address', {
    'line_1': fields.String(required=True, max_length=256, example="1234 Main Street"),
    'line_2': fields.String(required=True, max_length=256, example="Springfield"),
    'state': fields.String(required=True, max_length=2, example="IL"),
    'zip': fields.String(required=True, pattern=r'\d{5}', example="12345"),
})

PersonModel = api.model('Person', {
    'name': fields.String(required=True, max_length=64, example='John Williams'),
    'email': fields.String(required=True, pattern=r'[^@]+@[^@]+\.[^@]+', example='john.williams@email.com'),
    'phone': fields.String(required=True, pattern=r'\+?\d{10}', example='1234567890'),
    'address': fields.Nested(AddressModel, required=True),
})


@ns.route('/')
class Person(Resource):
    @ns.marshal_list_with(PersonModel)
    def get(self):
        """Retrieve all people"""

        return list(collection.find())

    @ns.expect(PersonModel)
    def post(self):
        """Create a person"""

        document = collection.insert_one(api.payload)
        return {"id": str(document.inserted_id)}


@ns.param('name', description="The name of the person being operated on.")
@ns.route('/name/<string:name>')
class PersonDetail(Resource):
    @api.marshal_with(PersonModel)
    def get(self, name):
        """Retrieve a person by name"""

        return collection.find_one({"name": name})

    @ns.expect(PersonModel)
    def put(self, name):
        """Update a person by name"""

        result = collection.replace_one({"name": name}, api.payload, upsert=False)
        return {'modified': f'{result.modified_count} record(s)'}

    def delete(self, name):
        """Delete a person by name"""

        result = collection.delete_one({"name": name})
        return {'deleted': f'{result.deleted_count} record(s)'}
