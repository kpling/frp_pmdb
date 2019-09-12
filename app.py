from flask import Flask, request
from flask_restplus import Api, Resource
from marshmallow import Schema, fields, validate
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient()
db = client.flask_app
people = db.people


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


@api.route('/person')
class Person(Resource):
    def post(self):
        person = PersonSchema().load(request.json)
        document = people.insert_one(person)
        return {"id": str(document.inserted_id)}


@api.route('/person/name/<string:name>')
class Person(Resource):
    def get(self, name):
        document = people.find_one({"name": name})
        person = PersonSchema().dump(document)
        return person

    def put(self, name):
        document = people.find_one({"name": name})
        person = PersonSchema().load(request.json)
        document.save(person)
        return person

    def delete(self, name):
        document = people.find_one({"name": name})
        return people.remove(document)
