''' controller and routes for users '''
import os
from flask import request, jsonify

# Remember that 'app' and 'mongo' are objects initialised in app/__init__.py
# mongo object will let us query our database
from app import app, mongo
import logger

# This file defines CRUD for the users database
# REMINDER: CRUD stands for Create, Read, Update and Delete and are the 
# 4 basic operations for persistent data storage


# Find the root path for the project - we can use the virtual environment that Docker creates for us
# Then we define a logger to output to ROOT/output.log
ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log'))

# Create a 'route', this is an entry into our database app.
# Allow the 4 CRUD operations
# Provide the mongo implementation for these 4
@app.route('/user', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def user():
    # GET (or read) Check the arguments for the query string
    # Search the database
    # Return the result as JSON
    if request.method == 'GET':
        query = request.args
        data = mongo.db.users.find_one(query)
        return jsonify(data), 200

    # The other three methods require data to be requested 
    data = request.get_json()

    # For a POST (or create), we need to validate that the provided data contains a name and email
    # If so, we can insert it into our database
    # If not, we output an error
    if request.method == 'POST':
        if data.get('name', None) is not None and data.get('email', None) is not None:
            mongo.db.users.insert_one(data)
            return jsonify({'ok': True, 'message': 'User created successfully!'}), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

    # For a DELETE, we need the user's email to uniquely identify them
    # Then attempt to delete the record in the database with that email
    if request.method == 'DELETE':
        if data.get('email', None) is not None:
            db_response = mongo.db.users.delete_one({'email': data['email']})
            if db_response.deleted_count == 1:
                response = {'ok': True, 'message': 'record deleted'}
            else:
                response = {'ok': True, 'message': 'no record found'}
            return jsonify(response), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

    # For a PATCH (or update), we check that the incoming data has a query and payload items
    # Modify the matched user with the data given in 'payload'
    if request.method == 'PATCH':
        if data.get('query', {}) != {}:
            mongo.db.users.update_one(
                data['query'], {'$set': data.get('payload', {})})
            return jsonify({'ok': True, 'message': 'record updated'}), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400