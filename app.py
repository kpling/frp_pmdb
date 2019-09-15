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
    'line_1': model_fields.String(max_length=256),
    'line_2': model_fields.String(max_length=256),
    'state': model_fields.String(max_length=2),
    'zip': model_fields.String(pattern=r'\d{5}'),
})

PersonModel = api.model('Person', {
    'name': model_fields.String(max_length=64),
    'email': model_fields.String(pattern=r'[^@]+@[^@]+\.[^@]+'),
    'phone': model_fields.String(pattern=r'\+?\d{10}'),
    'address': model_fields.Nested(AddressModel),
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


@ns.route('/name/<string:phone>')
class PersonPhoneDetail(Resource):
    def get(self, phone):
        """Retrieve a person by phone"""

        document = mongo.db.people.find_one({"phone": phone})
        return PersonSchema().dump(document)

    @ns.expect(PersonModel)
    def put(self, phone):
        """Update a person by phone"""

        try:
            person = PersonSchema().load(api.payload)
        except ValidationError as error:
            return error.messages

        # TODO: Handle no record exists
        mongo.db.people.update_one({"phone": phone}, {"$set": person})
        return {'modified': True}

    def delete(self, phone):
        """Delete a person by phone"""

        mongo.db.people.find_one({"phone": phone})
        return {'deleted': True}
