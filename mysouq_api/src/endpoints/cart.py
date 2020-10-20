from flask import Blueprint, jsonify, request
from datetime import datetime
from ..models import Cart, Product
from mongoengine import *
import json

# define the blueprint
cart_blueprint = Blueprint(name="cart_blueprint", import_name=__name__)

# note: global variables can be accessed from view functions
x = 5

# add view function to the blueprint


@cart_blueprint.route('/test', methods=['GET'])
def test():
    output = {
        "msg": "I'm the test endpoint from the tasklist blueprint."
    }
    return jsonify(output)

# add view tasklist function to the blueprint


@cart_blueprint.route('/<cart_id>', methods=['GET'])
def view_cart(cart_id):

    # Retrieve the tasklist
    cart = Cart.objects(id=cart_id).first()

    # Find all tasks for this tasklist
    products = Product.objects(carts__in=[cart]).all()

    # Load JSON from DB into JSON object
    json_cart = json.loads(cart.to_json())
    json_products = {"products": json.loads(products.to_json())}

    # Append tasks to tasklist
    json_cart.update(json_products)

    # Return JSON response

    return jsonify(json.dumps(json_cart))

# add create tasklist function to the blueprint


@ cart_blueprint.route('/create', methods=['POST'])
def create_carts():
    # Read JSON data from request from the client
    data = request.get_json()

    # Create and save a new task list
    cart = Cart(owner_id= data['user_id']).save()
    # Create test tasks
    product = Product(name="Demo product 1", description="First product on this list!",
                created_at=datetime.now(), carts=[cart]).save()
    product = Product(name="Demo product 2", description="Second product on this list!",
                created_at=datetime.now(), carts=[cart]).save()
    return product.to_json()

# add delete tasklist function to the blueprint


# @ tasklist_blueprint.route('/<tasklist_id>', methods=['delete'])
# def delete_tasklist(tasklist_id):

#     # Retrieve the tasklist
#     tasklist = TaskList.objects(id=tasklist_id).first()

#     if tasklist is not None:
#         tasklist.delete()
#         return jsonify({"msg": f"Task list {tasklist_id} has been deleted."})
#     else:
#         return jsonify({"msg": f"Task list {tasklist_id} does not exist."})

# add view tasklists function to the blueprint

@cart_blueprint.route('/own_cart')
def view_cart_all():

    # Retrieve the tasklist
    cart = Cart.objects()

    return cart.to_json()

# @tasklist_blueprint.route('/update/<tasklist_id>',methods=['PUT'])
# def update_tasklist(tasklist_id):

#     tasklist = TaskList.objects(id=tasklist_id).first()
#     # Read JSON data from request from the client
#     data = request.get_json()

#     tasklist.name=data['name']
#     tasklist.description=data['description']

#     tasklist.save()
#     return tasklist.to_json()
    


    # Update and save a new info task list
        # update_tasklist = data.keys()[0]
        # update_val = (tasklist for tasklist in data if tasklist['id'] == tasklist_id).next()[update_tasklist] = data.values()[0]
        # update_resp = (tasklist for tasklist in data if tasklist['id'] == tasklist_id).next()

    # tasklist=TaskList( name=data['name'],
    # description=data['description']).put()
    # return tasklist.to_json()

    #return jsonify({"msg": f"Task list {update_resp} has been updated."})

@cart_blueprint.route('/all')
def view_carts():

    # Retrieve the tasklist
    cart = Cart.objects()

    # Find all pages Bob authored
    cart.tasks = Product.objects(authors__in=[cart])

    return cart.to_json()
