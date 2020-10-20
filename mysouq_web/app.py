from flask import Flask, render_template, request, jsonify ,session ,redirect,url_for,flash
from wtforms import IntegerField ,StringField ,PasswordField,SubmitField,TextAreaField
from wtforms.validators import DataRequired ,Email ,Length
from flask_wtf import FlaskForm
import requests
import json
from flask_login import current_user ,login_user

class productForm(FlaskForm):
    maker = StringField('Maker', validators=[DataRequired()])
    model = StringField('Model', validators=[DataRequired()])
    img_link = StringField('Image Link', validators=[DataRequired()])
    specs = TextAreaField('Specifications')
    memory = IntegerField('Memory', validators=[DataRequired()])
    ram = IntegerField('RAM', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    submit = SubmitField('Add Phone')


class AddForm(FlaskForm):
    number = IntegerField('Number', validators=[DataRequired()])

class SignupForm(FlaskForm):
    username = StringField('username',validators=[DataRequired()])
    first_name =StringField('first_name',validators =[DataRequired()])
    last_name =StringField('last_name',validators =[DataRequired()])                                  
    email = StringField('Email',validators=[Length(min=6),Email(message='Enter a valid email.'),DataRequired()])
    address= StringField('address',validators=[DataRequired()])                                
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message='Select a stronger password.')])
    submit = SubmitField('signIn')

class LoginForm(FlaskForm):
    """User Login Form."""
    username = StringField('username', validators=[DataRequired()])                                        
    password = PasswordField('Password', validators=[DataRequired()])
    

class EditForm(FlaskForm):
    username = StringField('username',validators=[DataRequired()])
    first_name =StringField('first_name',validators =[DataRequired()])
    last_name =StringField('last_name',validators =[DataRequired()])                                  
    email = StringField('Email',validators=[Length(min=6),Email(message='Enter a valid email.'),DataRequired()])
    address= StringField('address',validators=[DataRequired()])                                
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message='Select a stronger password.')])

DEBUG = True
SECRET_KEY = 'secret'

app = Flask(__name__)
app.config.from_object(__name__)   

@app.route("/")
def index():
    return render_template('base.html')
                            
@app.route("/signup", methods=['GET','POST']) 
def signup():
    form = SignupForm()
    if request.method=='POST':
        data={'username':form.username.data,
            'first_name':form.first_name.data,
            'last_name':form.last_name.data,
            'email':form.email.data,
            'password':form.password.data,
            'address':form.address.data
        }
        # username = request.form('username')
        # first_name= request.form('first_name')
        # last_name= request.form('last_name')
        # password = request.form('password')
        # email=request.form('email')
        # address = request.form('address')
        
        result =requests.post('http://localhost:8080/api/v1/user/create',json=data)
        return redirect(url_for('login'))
    return render_template('signup.html',form=form)


    


        

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method=='POST':
        data={'username':form.username.data,
        'password':form.password.data
        }            
        session['is_logged_in'] = True
        return redirect(url_for('index'))
        result = requests.post('http://localhost:8080/api/v1/user/login',json=data)
    return render_template('login.html',form=form) 
    # if form.validate_on_submit():
    #     user = form.query.filter_by(username=form.username.data).first()
    #     if user is None or not user.check_password(form.password.data):
    #         flash('Invalid username or password')
    #         return redirect(url_for('login'))
    #     login_user(user, remember=form.remember_me.data)
    #     return redirect(url_for('index'))
    # return render_template('login.html', title='Sign In', form=form)


@app.route('/edit-profile',methods=['POST'])
def edit_user():
    form = EditForm()
   
    if request.method=='POST':
        data = {'username':form.username.data,
        'first_name':form.first_name.data,
        'last_name':form.last_name.data,
        'password':form.password.data 
        }
          
        #send the json data to the api 
        result = requests.post('http://localhost:8080/api/v1/user/edit-profile',json=data)
        print(data)
 
        return redirect(url_for('/'))
    
    return render_template('/profile/edit-profile.html',form=form)   





@app.route('/logout')
def logout():
    # clear the session 'user' attribute
    session.clear()
    
    # redirect to /
    return redirect(url_for('index'))

@app.route("/test/x")
def test_x():
    r = requests.get('http://localhost:8080/api/v1/path_for_blueprint_x/test')

    return r.json()


@app.route("/test/y")
def test_y():
    r = requests.get('http://localhost:8080/api/v1/path_for_blueprint_y/test')

    return r.json()


@app.route("/tasklists")
def tasklists():
    # Build JSON for API request
    data = {"user_id": "5f7af9b4f8f780280e44c0b2"}

    # Retrieve the user tasklists
    r = requests.post(
        'http://localhost:8080/api/v1/user/tasklists', json=data)

    # Render the tasklists view with the tasklists
    return render_template("tasklists.html", tasklists=r.json())


@app.route("/user/<user_id>")
def view_profile(user_id):
    # Retrieve task list data
    r = requests.get(
        'http://localhost:8080/api/v1/user/all' + user_id)

    user = json.loads(r.json())
    
    return render_template("profile/profile.html", user=user)


@app.route("/product" ,methods=['GET,POST'])
def add_product(user_id):
    form = productForm()
    if request.method=='POST':
        data={'maker':form.maker.data,
            'model':form.model.data,
            'img_link':form.img_link.data,
            'specs':form.specs.data,
            'memory':form.memory.data,
            'ram':form.ram.data,
            'price':form.price.data
        }
        result = requests.post('http://localhost:8080/api/v1/product/create',json=data)
        print(data)
 
        return redirect(url_for('/'))
    
    return render_template('add-product.html',form=form)   

@app.route("/product/<product_id>")
def view_product(product_id):
    
 
   #send the json data to the api 
    r = requests.get(
        'http://localhost:8080/api/v1/product/' + product_id)

    products = r.json()

    return render_template("view-product.html",products=products)
  




@app.route("/favorites")
def view_favorites():
    form = productForm()
    #store the data from the form as json
    data = {'title':form.title.data,
            'description':form.description.data
            
        }
    #send the json data to the api 
    r = requests.get(
        'http://localhost:8080/api/v1/product/favorites', json = data )
   
    items = r.json()
    
    return render_template("favorites-product.html",form=form, items=items)

@app.route("/search",methods=['GET','POST'])    
def search():
    form = productForm()
    if request.method == 'GET':
        return render_template("search/search.html",form=form)

    else: 

        #store the data from the form as json  
       
        data = {'title':form.title.data,
                'description':form.description.data,
                
                
            }
        #send the json data to the api 
        r = requests.post(
            'http://localhost:8080/api/v1/product/search', json = data )


    items = r.json()
   
      
    return render_template("search/result.html",items=items)

@app.route("/descending-sort",methods=['GET','POST'])    
def descending_sort():

    form = productForm()

    if request.method == 'GET':
        return render_template("sorting/dec-sort.html",form=form)

    else:   
        #store the data from the form as json   
        data = {'title':form.title.data,
                'description':form.description.data,
                'price':form.price.data
                
            }
        #send the json data to the api 
        r = requests.post(
            'http://localhost:8080/api/v1/product/des_sort', json = data )


    descending_items =r.json()
        
      
    return render_template("sort/result_sort.html",descending_items=descending_items)
        
@app.route("/ascending-sort",methods=['GET','POST'])    
def ascending_sort():

    form = productForm()

    if request.method == 'GET':
        return render_template("sort/asc-sort.html",form=form)

    else:   

        #store the data from the form as json         
        data = {'title':form.title.data,
                'description':form.description.data,
                'price':form.price.data
                
            }
        #send the json data to the api 
        r = requests.post(
            'http://localhost:8080/api/v1/item/asc-sort.html', json = data )

  
    ascending_product =r.json() 
  
      
     
    return render_template("sort/result-asc.html",ascending_product=ascending_product )

if __name__ == "__main__":
    app.run()