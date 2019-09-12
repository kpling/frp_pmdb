from flask import Flask, request
from flask_restplus import Api, Resource
from marshmallow import Schema, fields, validate
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/flask_app"
api = Api(app)
mongo = PyMongo(app)


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
        document = mongo.db.people.insert_one(person)
        return {"id": str(document.inserted_id)}


@api.route('/person/name/<string:name>')
class Person(Resource):
    def get(self, name):
        document = mongo.db.people.find_one_or_404({"name": name})
        person = PersonSchema().dump(document)
        return person

    def put(self, name):
        document = mongo.db.people.find_one({"name": name})
        person = PersonSchema().load(request.json)
        document.save(person)
        return person

    def delete(self, name):
        document = mongo.db.people.find_one({"name": name})
        mongo.db.people.remove(document)
        return {}
