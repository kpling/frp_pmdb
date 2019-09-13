from flask import Flask
from flask_restplus import Api, Resource
from flask_restplus import fields as model_fields  # workaround for presenting app in one module
from marshmallow import Schema, fields, validate
from marshmallow.exceptions import ValidationError
from flask_pymongo import PyMongo

app = Flask(__name__)
api = Api(app, version='0.1', title='Person API', description='Example CRUD API using a Person model')
app.config["MONGO_URI"] = "mongodb://localhost:27017/flask_app"
mongo = PyMongo(app)
ns = api.namespace('person', description='Operations related to people')

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


class AddressSchema(Schema):
    line_1 = fields.Str(required=True, validate=validate.Length(max=256))
    line_2 = fields.Str(validate=validate.Length(max=256))
    state = fields.Str(required=True, validate=validate.Length(max=2))
    zip = fields.Str(required=True, validate=validate.Regexp(r'\d{5}'))


class PersonSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(max=64))
    email = fields.Email(required=True)
    phone = fields.Str(required=True, validate=validate.Regexp(r'\+?\d{10}'))
    address = fields.Nested(AddressSchema(), required=True)


@ns.route('/')
class Person(Resource):
    @ns.expect(PersonModel)
    def post(self):
        """Create a person"""

        try:
            person = PersonSchema().load(api.payload)
        except ValidationError as error:
            return error.messages
        document = mongo.db.people.insert_one(person)
        return {"id": str(document.inserted_id)}


@ns.route('/name/<string:name>')
class PersonNameDetail(Resource):
    def get(self, name):
        document = mongo.db.people.find_one_or_404({"name": name})
        """Retrieve a person by name"""

        document = mongo.db.people.find_one({"name": name})
        return PersonSchema().dump(document)

    @ns.expect(PersonModel)
    def put(self, name):
        """Update a person by name"""

        try:
            person = PersonSchema().load(api.payload)
        except ValidationError as error:
            return error.messages

        # TODO: Handle no record exists
        document = mongo.db.people.update_one({"name": name}, {"$set": person})
        return document.raw_result

    def delete(self, name):
        """Delete a person by name"""

        document = mongo.db.people.find_one({"name": name})
        return mongo.db.people.remove(document)
        return mongo.db.people.remove(document)
