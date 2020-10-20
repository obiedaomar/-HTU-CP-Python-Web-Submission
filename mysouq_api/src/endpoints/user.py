from flask import Blueprint, jsonify, request
from datetime import datetime
from ..models import User, Cart
from mongoengine import *

# define the blueprint
user_blueprint = Blueprint(name="user_blueprint", import_name=__name__)

# add create user function to the blueprint


@user_blueprint.route('/create', methods=['POST'])
def create_user():
    # Read the request data from the client
    data = request.get_json()

    # Create and save a user to the DB
    user = User(username=data['username'],
                password=User.generate_hash(data['password']),
                first_name=data['first_name'],
                last_name=data['last_name'],
                created_at=datetime.now()
                ).save()

    return user.to_json()


@user_blueprint.route('/login', methods=['POST'])
def login():
    # Read the request data from the client
    data = request.get_json()

    # Read credentials from request
    username = data['username']
    password = data['password']

    # Authenticate the user
    if User.authenticate(username, password):
        # Add user to session
       
        response = {"msg": f"User {username} is now logged in."}
        return jsonify(response)
    else:
        response = {"msg": "Invalid credentials."}
        return jsonify(response)

# add user tasklists function to the blueprint
@user_blueprint.route('/update/<user_id>',methods=['PUT'])
def update_user(user_id):
    user = User.objects(id=user_id).first()
    # Read JSON data from request from the client
    data = request.get_json()
    

    # Update and save a new info task
        # update_task = data.keys()[0]
        # update_val = (task for task in data if task['id'] == task_id).next()[update_task] = data.values()[0]
        # update_resp = (task for task in data if task['id'] == task_id).next()
    user.first_name= data['first_name']
    user.last_name= data['last_name']
    user.password= data['password']
    user.save()
    
    return user.to_json()
    #return jsonify({"msg": f"Task {update_resp} has been updated."})

@user_blueprint.route('/changepassword',methods=['PUT'])
def change_password(user_id):

    user = User.objects(id=user_id).first()
    # Read JSON data from request from the client
    data = request.get_json()
    user.password= data['password']
    user.save
    return user.to_json()




@user_blueprint.route('/carts', methods=['POST'])
def user_carts():
    data = request.get_json()

    # Retrieve the tasklist
    carts = Cart.objects(owner_id=data['user_id']).all()

    return carts.to_json()
