from flask import Flask, request
from flask_restplus import Api, Resource
from marshmallow import Schema, fields, validate
from flask_pymongo import PyMongo

app = Flask(__name__)
api = Api(app, version='0.1', title='Person API', description='Example CRUD API using a Person model')
app.config["MONGO_URI"] = "mongodb://localhost:27017/flask_app"
mongo = PyMongo(app)
ns = api.namespace('person', description='Operations related to people')


class AddressSchema(Schema):
    line_1 = fields.Str(validate=validate.Length(max=256))
    line_2 = fields.Str(validate=validate.Length(max=256))
    state = fields.Str(validate=validate.Length(max=2))
    zip = fields.Str(validate=validate.Regexp(r'\d{5}'))


class PersonSchema(Schema):
    name = fields.Str(validate=validate.Length(max=64))
    email = fields.Email()
    phone = fields.Str(validate=validate.Regexp(r'\+?\d{10}'))
    address = fields.Nested(AddressSchema())


@ns.route('/')
class Person(Resource):
    def post(self):
        person = PersonSchema().load(request.json)
        if mongo.db.people.find_one({'name': person.get('name')}):
            return {"error": "record already exists"}
        document = mongo.db.people.insert_one(person)
        return {"id": str(document.inserted_id)}


class Person(Resource):
@ns.route('/name/<string:name>')
    def get(self, name):
        document = mongo.db.people.find_one_or_404({"name": name})
        return PersonSchema().dump(document)

    def put(self, name):
        person = PersonSchema().load(request.json)
        document = mongo.db.people.update_one({"name": name}, {"$set": person})
        return document.raw_result

    def delete(self, name):
        document = mongo.db.people.find_one_or_404({"name": name})
        return mongo.db.people.remove(document)
