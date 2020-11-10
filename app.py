# importing libraries
from flask import Flask, Response, request
from settings.security import authenticate, identity
from flask_jwt import JWT, jwt_required, current_identity
import json
from bson.objectid import ObjectId
import config

# setting up app
app = Flask(__name__)
app.secret_key = 'hiiamyoursecret'
jwt = JWT(app, authenticate, identity)


# Functions for CRUD
@app.route('/create', methods=["POST"])
@jwt_required()
def create_employee():
    """
    To create employee
    :return: sucess/error msg with status code
    """
    try:
        emp = {'Name': request.form['Name'],
               'Email': request.form['Email'],
               'Company': request.form['Company'],
               'Salary': request.form['Salary']
               }
        dbResponse = config.Db.conf().insert_one(emp)
        return Response(response=json.dumps(
            {"message": "user created", "id": f"{dbResponse.inserted_id}"}),
            status=200,
            mimetype="application/json")
    except Exception as e:
        return Response(response=json.dumps({"message": "Not able to create employee"}), status=500,
                        mimetype="application/json")


@app.route('/getall', methods=["GET"])
def get_employees():
    """
    To get all employee
    :return: if success get all employee with status code or failur with status code
    """
    try:
        data = list(config.Db.conf().find())
        for user in data:
            user['_id'] = str(user['_id'])
        return Response(response=json.dumps(data), status=200, mimetype="application/json")
    except:
        return Response(response=json.dumps({"message": "Not able to get employee data"}), status=500,
                        mimetype="application/json")


@app.route('/update/<id>', methods=["PUT"])
@jwt_required()
def employee_update(id):
    """
    To update employee data
    :param id: object id
    :return: return updated msg with status code or failure msg with  status code
    """
    try:
        dbResponse = config.Db.conf().update_one({"_id": ObjectId(id)},
                                                 {"$set": {'Name': request.form['Name']}})
        if dbResponse.modified_count == 1:
            return Response(response=json.dumps({"message": "Employee details updated"}),
                            status=200,
                            mimetype="application/json")
    except:
        return Response(
            response=json.dumps({"message": "Unable to update employee"}),
            status=500,
            mimetype="application/json")


@app.route('/delete/<id>', methods=['DELETE'])
@jwt_required()
def delete_employee(id):
    """
    To delete employee record
    :param id: object id
    :return: deleted or failed with status code
    """
    try:
        dbResponse = config.Db.conf().delete_one({"_id": ObjectId(id)})

        return Response(response=json.dumps({"message": "employee details deleted"}),
                        status=200,
                        mimetype="application/json")
    except:
        return Response(
            response=json.dumps({"message": "Unable to delete employee"}),
            status=500,
            mimetype="application/json")


if __name__ == '__main__':
    app.run(port=5000, debug=True)
