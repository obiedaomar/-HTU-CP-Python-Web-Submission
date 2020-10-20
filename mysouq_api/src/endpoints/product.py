from flask import Blueprint, jsonify, request
from ..models import Product
from datetime import datetime
from ..models import Cart

# define the blueprint
product_blueprint = Blueprint(name="product_blueprint", import_name=__name__)

# note: global variables can be accessed from view functions
y = 5

# add view function to the blueprint


@product_blueprint.route('/test', methods=['GET'])
def test():
    output = {"msg": "I'm the test endpoint from blueprint_y."}
    return jsonify(output)

# add view function to the blueprint


@product_blueprint.route('/subtract', methods=['POST'])
def subtract_y():
    # retrieve body data from input JSON
    data = request.get_json()
    in_val = data['number']
    # compute result and output as JSON
    result = in_val - y
    output = {"msg": f"Your result is: '{result}'"}
    return jsonify(output)


@product_blueprint.route('/create', methods=['POST'])
def create_product():
    # Read JSON data from request from the client
    data = request.get_json()

    # Create and save a new product list
    product = Product(
        name=data['name'],
        description=data['description'],
        price = data['price'],
        created_at=datetime.now(),
        
    ).save()

    return product.to_json()
@product_blueprint.route('/<product_id>', methods = ['GET'])
def view_product(product_id):

    # Retrieve the item
    product = Product.objects(id = product_id)
   
    return product.to_json()


# add delete task function to the blueprint
@product_blueprint.route('/delete/<product_id>', methods=['delete'])
def delete_task(product_id):

    # Retrieve the task
    product = Product.objects(id=product_id).first()

    if product is not None:
        product.delete()
        return jsonify({"msg": f"product {product_id} has been deleted."})
    else:
        return jsonify({"msg": f"product {product_id} does not exist."})


# add view tasks function to the blueprint
@product_blueprint.route('/all' ,methods=['GET'])
def view_products():

    # Retrieve the task
    product = Product.objects()

    return product.to_json()

@product_blueprint.route('/update/<product_id>',methods=['PUT'])
def update_product(product_id):
    product = Product.objects(id=product_id).first()
    # Read JSON data from request from the client
    data = request.get_json()
    

    # Update and save a new info task
        # update_task = data.keys()[0]
        # update_val = (task for task in data if task['id'] == task_id).next()[update_task] = data.values()[0]
        # update_resp = (task for task in data if task['id'] == task_id).next()
    product.name= data['name']
    product.description= data['description']
    product.price= data['price']
    

    product.save()
    
    return product.to_json()
    #return jsonify({"msg": f"Task {update_resp} has been updated."})

# add favorite item function to the blueprint
@product_blueprint.route('/favorite/<product_id>',methods=['GET'])
def set_favorite(product_id):

    # Retrieve the item
    product=Product.objects(id=product_id).first()

    if product.is_favorite == True:

        product.is_favorite = False
    else:
        product.is_favorite = True
    
    product.save()
    return product.to_json()

# add favorite item function to the blueprint
@product_blueprint.route('/favorites' ,methods=['GET'])
def view_favorites():

    # Retrieve the item
    favorites_product = Product.objects(is_favorite = True)
    
    return favorites_product.to_json()

# add search item function to the blueprint
@product_blueprint.route('/search', methods =['GET', 'POST'])
def search():

    # Retrieve the item
    product = Product.objects.search_text('product')
    print(product)
    # items.title
    # if 'title' in request.args:
    #     items= items(title = request.args['title'])
     
    # if 'description' in request.args:
    #     items= items(description = request.args['description'])   
    return product.to_json()

# add descending sort item function to the blueprint
@product_blueprint.route('/des_sort',methods=['GET','POST'])   
def des_sort():


    # Retrieve the item
    descending_product = Product.objects().order_by('-price')
   
    return descending_product.to_json() 


# add ascending sort item function to the blueprint
@item_blueprint.route('/asc-sort',methods=['GET','POST'])   
def ascending_sort():


    # Retrieve the item
    ascending_product = Product.objects().order_by('+price')
    
    return ascending_product.to_json() 
