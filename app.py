import json, os
from bson.json_util import dumps
from bson.objectid import ObjectId

from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from pymongo import  TEXT
from marshmallow import Schema, fields
app = Flask(__name__)
mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/Data_API")
db = mongodb_client.db

class Company(Schema):
    company_id = fields.Integer()
    company_name = fields.String()
    company_address = fields.String()
    zipcode = fields.Integer()

class Employee(Schema):
    user_name = fields.String()
    email = fields.Email()
    mobile_number = fields.Integer()
    company = fields.Nested(Company, load_only=True)
    user_address = fields.String()

@app.route("/create", methods =[ 'POST'])
def add_one():
    data = request.args
    user_name = data.get('user_name')
    email = data.get('email')
    company_name = data.get('company_name')
    company_id= data.get('company_id')
    company_address = data.get('company_address')
    zipcode = data.get('zipcode')
    mobile_number = data.get('mobile_number')
    user_address = data.get('user_address')
    db.test.create_index("email", unique=True)
    last_name =None
    first_name , last_name = user_name.split(' ', 1)
    if find_user(db.employee.find({}), email) :
        return jsonify(message='mobile number is already exited ')
    elif find_mobile(db.employee.find({}), mobile_number):
        return jsonify(message='mobile number is already exited ')
    else:
        db.employee.insert_one({ 'first_name': first_name, 'last_name': last_name, 'mobile_number': mobile_number,
                                'email': email, 'user_address' : user_address,
                                'company':{'company_name':company_name, 'company_id': company_id,'zipcode': zipcode,'address': company_address}})

        return jsonify(message='success')

@app.route('/')
@app.route('/all_data')
def all_data():
    return   jsonify({"data":str([data for data in db.employee.find()])})

@app.route('/update/<email>', methods=['PUT'])
def update(email):
    data = request.args
    db.employee.create_index("email", unique=True)
    user_address = data.get('user_address')
    mobile_number = data.get('mobile_number')
    company_id = data.get('company_id')


    if find_user(db.employee.find(), email)  :
        if find_mobile(db.employee.find({}), mobile_number):
            return jsonify(message='mobile number is already exited ')
        db.employee.update_one({'email': email},
                           update={"$set": {'mobile_number': mobile_number, 'company_id':company_id,
                                            'user_address': user_address, }})
        return jsonify(message = 'Success')
    return jsonify(message = 'mail is not in db')

@app.route('/delete/<email>', methods=['DELETE'])
def delete_user(email):

    if find_user(db.employee.find(), email):
        db.employee.delete_one({'email': email})
        resp = jsonify('User deleted successfully!')
        resp.status_code = 200
        return resp
    return jsonify(message='Mail Id not found')

def find_user(data, user):
    for row in data:
        if row['email']== user:
            return True
    return False

def find_mobile(data, mobile):
    for row in data:
        if  str(row['mobile_number'] ) == str(mobile):
            return True
    return False
if __name__ == '__main__':
    app.run(debug=True)