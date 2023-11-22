from flask import Flask, render_template, request,session,redirect,flash,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from uuid import uuid4
from flask_mail import Mail, Message
import os
from werkzeug.utils import secure_filename
from random import randint



# app = Flask(__name__)
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/Swm'
app.config['SECRET_KEY'] = "Your_secret_string"

db = SQLAlchemy(app)

# for the customer
class customer(db.Model):
   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    date = db.Column(db.String(12), nullable=True)

# for the employee
class employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    Token = db.Column(db.String(80), nullable=True)
    date = db.Column(db.String(12), nullable=False)
    phone = db.Column(db.String(80), nullable=False)

# for the products
class item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=True)
    slug = db.Column(db.String(80), nullable=False)
    img = db.Column(db.String(80), nullable=True)
    description = db.Column(db.String(80), nullable=True)
    category = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=True)
    date = db.Column(db.String(12), nullable=True)
    emailE = db.Column(db.String(12), nullable=True)
    token = db.Column(db.String(80), nullable=True)


# for the ddcrt
class cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=True)
    username = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    Token = db.Column(db.String(80), nullable=True)
    prize = db.Column(db.Integer, nullable=True)
    quantity = db.Column(db.Integer, nullable=False)

    date = db.Column(db.String(12), nullable=False)
    
# for the orders
class placing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    productname = db.Column(db.String(80), nullable=False)
    productquantity = db.Column(db.String(80), nullable=False)
    producttoken = db.Column(db.Integer, nullable=False)
    productcategory = db.Column(db.Integer, nullable=True)
    otp = db.Column(db.Integer, nullable=True)
    img = db.Column(db.String(80), nullable=True)
    address = db.Column(db.String(80), nullable=True)
    prize = db.Column(db.String(80), nullable=True)
    phone = db.Column(db.Integer, nullable=True)
    date = db.Column(db.String(12), nullable=False)
    recname = db.Column(db.Integer, nullable=True)
    empphone = db.Column(db.Integer, nullable=True)
    companyname = db.Column(db.String(80), nullable=True)
    websitename = db.Column(db.String(80), nullable=True)
    gstnumber = db.Column(db.String(80), nullable=True)
    pan = db.Column(db.String(80), nullable=True)
    tan = db.Column(db.String(80), nullable=True)
    shipping = db.Column(db.String(80), nullable=False)

# for the contct
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    msg = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(12), nullable=False)
    


# Email
mail = Mail(app) # instantiate the mail class 
   
# configuration of mail 
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'pm550639@gmail.com'
app.config['MAIL_PASSWORD'] = 'tube filh gdgl rxmc'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app) 

@app.route("/")
def home():
    if 'user' in session:
        items = item.query.filter_by().all()
        return render_template('index.html',name = session['user'],item=items,homen='active')
    
    if 'userE' in session:
        items = item.query.filter_by().all()
        return render_template('dashboard.html',name = session['userE'],item=items)
    
    items = item.query.filter_by().all()[0:8]
    return render_template('index.html',item=items,homen='active')

# all produts looks
@app.route("/product")
def Allproduct():
    if 'user' in session:
        items = item.query.filter_by().all()
        return render_template('AllProducts.html',name = session['user'],item=items,productn='active')
    items = item.query.filter_by().all()
    return render_template('AllProducts.html',item=items,productn='active')


@app.route("/about")
def about():
    if 'user' in session:
        return render_template('about.html',name = session['user'],aboutn='active')
    return render_template('about.html',aboutn='active')



@app.route("/contact",methods = ['GET','POST'])
def contact():
    if request.method=="POST":
            name = request.form.get('name')
            phone = request.form.get('phone')
            email = request.form.get('email')
            mesg = request.form.get('msg')
            entry = Contact(name=name, phone=phone,email=email, msg= mesg ,date=datetime.now())
            db.session.add(entry)
            db.session.commit()
            msg = Message("SWM Feedback",
                          sender="pm550639@gmail.com",
                          recipients=[email])
            msg.body = 'Hello ' + name + ','
            # Assuming 'msg' is a list
            msg.html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Feedback</title>
            </head>
            <body>
                <h2>Your token here</h2>
                <h3>Name:{name}</h3>
                <h5>Phone NO:{phone}</h5>
                <h5>Email:{email}</h5>
                <h5>Message:{mesg}</h5>
                <h5>Date:{datetime.now()}</h5>
            </body>
            </html>
            """

            mail.send(msg)

            return render_template('contact.html',success = "Your message has been sent",act = "block",contactn='active',name = session['user'])

    return render_template('contact.html',contactn='active')



# product on showing             oky              
@app.route("/item/<string:post_slug>",methods = ['GET'])
def product(post_slug):
    items = item.query.filter_by(slug=post_slug).first()

    if items.quantity == 0 or items.quantity < 0:
        # items = item.query.filter_by(slug=post_slug).first()
        return render_template('product.html', item=items,name = session['user'],sold= "Sold Out",productn='active')

    return render_template('product.html',item=items,productn='active')


@app.route("/item/<string:post_slug>/<string:id>", methods=['GET', 'POST'])
def cartadd(post_slug, id):
    item_to_add = item.query.filter_by(id=id, slug=post_slug).first()

    if 'user' in session:
        if request.method == "POST":
            quantity = int(request.form.get('quantity'))
            if quantity <= 0:
                print("\n\n\n\n\n\n\n\n\nnull\n\n\n\n\n\n\n\n")
                quantity = 1
            elif item_to_add.quantity < quantity:
                return render_template('product.html', item=item_to_add, error="Sorry, we don't have that much quantity available.")

            entry = cart(
                name=item_to_add.name,
                username=session['userEmail'],
                prize=quantity * item_to_add.price,
                date=datetime.now(),
                quantity=quantity,
                category=item_to_add.category,
                Token=item_to_add.token
            )
            db.session.add(entry)
            db.session.commit()

            carts = cart.query.filter_by(username=session['userEmail']).all()

            if carts:
                items = item.query.filter_by().all()
                return render_template('AllProducts.html',name = session['user'],item=items, success ="This product is in your cart.",productn='active')

    else:
        return redirect('/signin')    

    return render_template('product.html', item=item_to_add,productn='active')


# add cart All conecpts                    
@app.route("/addcart")
def addcart():
    if 'user' in session:
        items = item.query.filter_by().all()
        carts = cart.query.filter_by(username=session['userEmail']).all()
        return render_template('addtocart.html',item=items,carts=carts,name=session['user'],productn='active')
    else:
        return render_template('login.html', error="Something went wrong. If you have an account, please log in.")


# crt product delete
@app.route("/remove_from_cart/<string:id>",methods = ['GET','POST'])
def delproductincart(id):
    carts = cart.query.filter_by(id=id).first()
    if cart:
        db.session.delete(carts)
        db.session.commit()

    return redirect('/addcart')


@app.route("/update_cart/<string:id>",methods = ['GET','POST'])
def update_cart(id):
    if 'user' in session or 'userEmail' in session:
        carts = cart.query.filter_by(id=id).first()
        if request.method == 'POST':
        # Retrieve user input
            quantity = int(request.form.get('quantity'))
            prize = quantity* carts.prize 
            carts.quantity = quantity
            carts.prize = prize 
            db.session.commit()
            
            return redirect("/addcart")
    
    

# checkout options 
@app.route("/checkout",methods = ['GET','POST'])
def checkout():
    if 'user' in session or 'userEmail' in session:

        # items = item.query.filter_by(token = token).all()
        carts = cart.query.filter_by(username=session['userEmail']).all()
        total_prize = sum(cart.prize for cart in carts)
         # Calculate the total quantity
        total_quantity = sum(cart.quantity for cart in carts)

        return render_template('checkout.html',carts=carts,username = session['userEmail'],total_prize=total_prize,total_quantity=total_quantity)
    else:
        return render_template('login.html', error="Something went wrong. If you have an account, please log in.")
 


def render_error(error_message):
    carts = cart.query.filter_by(username=session['userEmail']).all()
    total_prize = sum(cart.prize for cart in carts)
         # Calculate the total quantity
    total_quantity = sum(cart.quantity for cart in carts)
    return render_template('checkout.html', carts=carts, username=session['userEmail'], total_prize=total_prize, total_quantity=total_quantity, error=error_message)

# for the user
# @app.route("/placing", methods=['GET', 'POST'])
# def place_order():
#     if 'user' in session:
#         if request.method == 'POST':
#             # Retrieve user input
#             normlre = 0
#             phone = request.form.get('phone')
#             recname = request.form.get('recname')
#             address = request.form.get('address')
#             cardnum = request.form.get('cardnum')
#             expiration = request.form.get('expiration')
#             cvv = request.form.get('cvv')

#             print(f"\n\n\n\n\n\n\n\n {phone, recname, address}\n\n\n\n\n\n\n\n")
#             carts = cart.query.filter_by(username=session['userEmail']).all()
#             if len(phone) != 10:
#                 return render_error("Your phone number is not correct")
#             if len(recname) <= 5:
#                 return render_error("Your name is not correct")
#             if len(cardnum) != 16:
#                 return render_error("Your Card Number is not valid")
#             if len(expiration) < 3:
#                 return render_error("Expiration date is not in the correct format (MM/YY)")
#             if len(cvv) != 3:
#                 return render_error("CVV is not in the correct format")
        


#             cart_items = cart.query.filter_by(username=session['userEmail']).all()

#             try:
#                 for cart_item in cart_items:
#                     items = item.query.filter_by(token=cart_item.Token).first()

#                     if items.token == cart_item.Token:
#                         print(f"\n\n\n\n\n\n\n\nit is two item.token :{items.token} \n\n cart_items.token: {cart_item.Token} \n\n\n\n\n\n\n\n")
#                         if items.quantity >= cart_item.quantity:
#                             items.quantity -= cart_item.quantity
#                             db.session.commit()
#                     ot = uuid4()
#                     otp = str(ot)[:5]
#                     entry = placing(
#                         username=session['userEmail'],
#                         productname=cart_item.name,
#                         productquantity=cart_item.quantity,
#                         prize=cart_item.prize,
#                         date=datetime.now(),
#                         productcategory=cart_item.category,
#                         otp = otp,
#                         producttoken=cart_item.Token,
#                         address=address,
#                         recname=recname,
#                         phone=phone
#                     )
#                     db.session.add(entry)
#                     normlre = 1


#                 for cart_item in cart_items:
#                     db.session.delete(cart_item)
#                     db.session.commit()
#                     normlre = 1
#                 # Commit all entries after the loop
#                 db.session.commit()
                
#                 # Execute code before the redirect
#                 if normlre == 1:
#                     print("\n\n\n\n\n\n\n\n\n\n order \n\n\n\n\n\n\n\n\n")
#                     print("\n\n\n\n\n\n\n\n\n\n Before redirect \n\n\n\n\n\n\n\n\n\n")
#                     return redirect('/Order')  # Redirect here
#                 else:
#                     return render_error("ny item you should slect on crt")


#             except Exception as e:
#                 print(f"\n\n\n\n\n\n\n\n {e}\n\n\n\n\n\n\n\n")
#                 return render_template("checkout.html", error=e)
#         else:
#             return render_template('login.html', error="Something went wrong. If you have an account, please log in.")
#             # ...
#     else:
#         return render_template('login.html', error="Something went wrong. If you have an account, please log in.")


@app.route("/placing", methods=['GET', 'POST'])
def place_order():
    if 'user' in session:
        if request.method == 'POST':
            # Retrieve user input
            normlre = 0
            phone = request.form.get('phone')
            recname = request.form.get('recname')
            companyname = request.form.get('companyname')
            websitename = request.form.get('websitename')
            gstnumber = request.form.get('gstnumber')
            pan = request.form.get('pan')
            tan = request.form.get('phone')
            address = request.form.get('address')
            cardnum = request.form.get('cardnum')
            expiration = request.form.get('expiration')
            cvv = request.form.get('cvv')
            shipping = request.form.getlist('shipping')
            


            print(f"\n\n\n\n\n\n\n\n {shipping}\n\n\n\n\n\n\n\n")
            carts = cart.query.filter_by(username=session['userEmail']).all()
            if len(phone) != 10:
                return render_error("Your phone number is not correct")
            if len(companyname) < 2:
                return render_error("Put Company Name is not in the format")
            if len(gstnumber) < 3:
                return render_error("Put Gst Number is not in the format")
            if len(pan) < 3:
                return render_error("Put Pan Number is not in the format")
            if len(tan) < 3:
                return render_error("Put Tan Number is not in the format")
            if len(recname) <= 5:
                return render_error("Your name is not correct")
            if len(cardnum) != 16:
                return render_error("Your Card Number is not valid")
            if len(expiration) < 3:
                if ((expiration[0:2]) <= 31 and expiration[3:5] > 23):
                    return render_error("Expiration date is not in the correct format (MM/YY)")
            if len(cvv) != 3:
                return render_error("CVV is not in the correct format")
        


            cart_items = cart.query.filter_by(username=session['userEmail']).all()

            try:
                for cart_item in cart_items:
                    items = item.query.filter_by(token=cart_item.Token).first()

                    if items.token == cart_item.Token:
                        print(f"\n\n\n\n\n\n\n\nit is two item.token :{items.token} \n\n cart_items.token: {cart_item.Token} \n\n\n\n\n\n\n\n")
                        if items.quantity >= cart_item.quantity:
                            items.quantity -= cart_item.quantity
                            db.session.commit()
                    ot = uuid4()
                    otp = str(ot)[:5]
                    entry = placing(
                        username=session['userEmail'],
                        productname=cart_item.name,
                        productquantity=cart_item.quantity,
                        prize=cart_item.prize,
                        date=datetime.now(),
                        productcategory=cart_item.category,
                        otp = otp,
                        producttoken=cart_item.Token,
                        address=address,
                        recname=recname,
                        phone=phone,
                        companyname=companyname,
                        websitename=websitename,
                        gstnumber=gstnumber,
                        pan=pan,
                        tan=tan,
                        shipping = shipping,
                        img = items.img


                    )
                    db.session.add(entry)
                    normlre = 1


                for cart_item in cart_items:
                    db.session.delete(cart_item)
                    db.session.commit()
                    normlre = 1
                # Commit all entries after the loop
                db.session.commit()
                
                # Execute code before the redirect
                if normlre == 1:
                    print("\n\n\n\n\n\n\n\n\n\n order \n\n\n\n\n\n\n\n\n")
                    print("\n\n\n\n\n\n\n\n\n\n Before redirect \n\n\n\n\n\n\n\n\n\n")
                    return redirect('/Order')  # Redirect here
                else:
                    return render_error("any item you should select on cart")


            except Exception as e:
                print(f"\n\n\n\n\n\n\n\n {e}\n\n\n\n\n\n\n\n")
                return render_template("checkout.html", error=e)
        else:
            return render_template('login.html', error="Something went wrong. If you have an account, please log in.")
            # ...
    else:
        return render_template('login.html', error="Something went wrong. If you have an account, please log in.")

# checkout options 
@app.route("/Order",methods = ['GET','POST'])
def Order():
    if 'user' in session or 'userEmail' in session:
        Placing = placing.query.filter_by(username=session['userEmail']).all() 
        if Placing:
            return render_template('Order.html',name=session['user'], success="your placing order is successfully",placing=Placing,Ordern='active')
        else:
            return redirect("/")
    else:
        return render_template("login.html",error_message = "Do signin First")
 

@app.route("/Cancel/<string:id>", methods=['GET', 'POST'])
def cancel_order(id):
    if request.method == "POST":
        Placing = placing.query.filter_by(id=id).first()
        if Placing:
            items = item.query.filter_by(token=Placing.producttoken).first()
            items.quantity += Placing.productquantity
            msg = Message("SWM Cancel(Refund)",
                          sender="pm550639@gmail.com",
                          recipients=[session['userEmail']])
            msg.body = 'Hello ' + session['user'] + ','
            msg.html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Feedback</title>
            </head>
            <body>
                <h2>Refund Money</h2>
                <h3>Name:{Placing.productname}</h3>
                                <h5>Rec_Name:{Placing.recname}</h5>

                <h5>Phone NO:{Placing.phone}</h5>
                <h5>here tht mount who send tht money {Placing.prize} to tht number </h5>
                                <h5>Product_Token:{Placing.producttoken}</h5>

                <h5>Date:{datetime.now()}</h5>
            </body>
            </html>
            """
            mail.send(msg)
            msgC = Message("SWM Cancel",
                          sender=session['userEmail'],
                          recipients=["pm550639@gmail.com"])
            msgC.body = 'Hello ' + session['user'] + ','
            msgC.html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Your amout will be provide you in 4 days</title>
            </head>
            <body>
                <h2>Your amout will be provide you in 4 days</h2>
                <h5>here money {Placing.prize} </h5>
            </body>
            </html>
            """
            mail.send(msgC)
            db.session.delete(Placing)
            db.session.commit()

            return redirect('/Order')
        else:
            return render_template('Order.html', username=session['user'], error="Order not found or cannot be canceled.",Ordern='active')

    else:
        Placing = placing.query.filter_by(username=session['userEmail']).all()
        return render_template('Order.html', username=session['user'], placing=Placing,Ordern='active')



# dashboards employee all concepts

@app.route("/dashboard")
def dashboard():
    if 'userE' in session:
        items = item.query.filter_by().all()
        return render_template("dashboard.html",item=items,user=session['userE'])
    else:
        return redirect('/signin')


@app.route("/edit/<string:id>",methods = ['GET','POST'])
def editproduct(id):
    if request.method=="POST":
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        emailE = request.form.get('emailE')
        category = request.form.get('category')
        quantity = request.form.get('quantity')

        items = item.query.filter_by(id=id).first()

        items.name = name
        items.description = description
        items.price = price
        items.emailE = emailE
        items.date = datetime.now()
        items.category = category
        items.quantity = quantity
        db.session.commit()
        return redirect('/dashboard')
    items = item.query.filter_by(id=id).first()
    return render_template('editp.html',item=items)


@app.route("/uploader", methods=["GET","POST"])
def uploader():
    if request.method == 'POST':
        image = request.files['file1']
        if image:
            if image.filename != '':
                # Secure the filename to prevent malicious input
                filename = secure_filename(image.filename)

                # Extract the original file extension
                file_extension = os.path.splitext(filename)[1]

                # Generate a new filename with a timestamp and the original extension
                timestamped_filename = 'item_' + str(randint(0000000,99999999)) + file_extension

                # Set the complete path to save the file
                image_path = os.path.join('/home/parth/Desktop/New Folder/env/static/item', timestamped_filename)

                # Save the file to the specified folder
                image.save(image_path)

                # Get other product information from the form
                name = request.form.get('name')
                description = request.form.get('description')
                price = request.form.get('price')
                emailE = request.form.get('emailE')
                category = request.form.get('category')
                quantity = request.form.get('quantity')

                try:
                    # Add the entry to the database, including the image filename
                    entry = item(
                        name=name,
                        description=description,
                        price=price,
                        date=datetime.now(),
                        emailE=emailE,
                        quantity=quantity,
                        slug=f'slug{uuid4()}',
                        category=category,
                        token=uuid4(),
                        img=timestamped_filename  # Add this field for the image filename
                    )
                    session['userE'] = emailE
                    db.session.add(entry)
                    db.session.commit()
                    return render_template("dashboard_form.html", error="Product and image uploaded successfully!",user=session['userE'])
                except Exception as e:
                    print(f"\n\n\n\n\n\n\n\nerrot: {e} \n\n\n\n\n\n\n\n")
                    return render_template("dashboard_form.html", error=e,user=session['userE'])

    return render_template("dashboard_form.html",user=session['userE'])


@app.route("/AllPlacing")
def AllPlacing():
    if 'userE' in session:
        Placing = placing.query.all() 
        return render_template("AllPlacing.html",placing=Placing,user=session['userE'],delbutton="hidden")
    else:
        return redirect('/signin')


@app.route("/AllPlacing/<string:producttoken>",methods = ['GET','POST'])
def AllPlacingdel(producttoken):
    Placing = placing.query.filter_by(producttoken=producttoken).first()
    if cart:
        db.session.delete(Placing)
        db.session.commit()

    return redirect('/AllPlacing')

# login all concepts

@app.route("/signin", methods = ['GET', 'POST'])
def signin():
    if 'user' in session:
        return redirect('/')


    if request.method == 'POST':
        usernameu = request.form.get('username')
        password = request.form.get('password')

        user = customer.query.filter_by(username=usernameu).first()
        print(f"\n\n\n\n\n\n\nhere mybe {user}  \n\n\n\n\n\n\n\n\n\n\n\n\n {password}\n\n\n\n\n\n")

        if user:
            if user and user.password == str(password):
                # Password matches
                print("\n\n\n\n\n\n\nhere mybe\n\n\n\n\n\n")
                session['user']=user.name
                session['userEmail']=user.username

                return redirect('/')
            else:
                # Password does not match
                return render_template('login.html', error_message="Incorrect username or password")
        return render_template('login.html', error_message="Provide username or password")

    return render_template('login.html')


@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    if(request.method=='POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        print(f"\n\n\n\n\n\n\n emp dimg  {username} {password} \n\n\n\n\n\n\n\n\n")
        if username and password:
            entry = customer(name=name, username=username,password=password, date= datetime.now())
            session['user'] = name
            session['userEmail']=username
            db.session.add(entry)
            db.session.commit()
            return redirect('/')
        else:
            return render_template('login.html', error_message="Provide username or password")


    return redirect('/signin')


@app.route("/emp", methods = ['GET', 'POST'])
def Emp():
    if 'userE' in session:
        return render_template("dashboard.html")
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            checkemp = employee.query.filter_by(username=username).first()
        except Exception as e:
            print(f"\n\n\n\n\n\n error checkemp: {e} \n\n\n\n\n\n")
        
        t = str(randint(000000,999999))
        if checkemp:
            if checkemp.password ==  password:
                token = t
                checkemp.Token = token
                checkemp.date = datetime.now()
                db.session.commit()
                msg = Message("SWM Token Service",
                            sender="pm550639@gmail.com",
                            recipients=[username])
                msg.body = 'Hello ' + checkemp.name + ','
                msg.html = """
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Token</title>
                </head>
                <body>
                    <h2>Your token here</h2>
                    <h3>{}</h3>
                </body>
                </html>
                """.format(token)
                mail.send(msg)

                            
                return redirect('/verify')                
            else:
                # Password does not match
                return render_template('login.html', error_message="Incorrect username or password")
        return render_template('login.html', error_message="Provide username or password")

    return render_template('login.html', error_message="Incorrect username or password")

@app.route("/verify", methods = ['GET', 'POST'])
def verify():
    if(request.method=='POST'):
        '''Add entry to the database'''
        Token = request.form.get('token')
        checkT = employee.query.filter_by(Token=Token).first()
        if (checkT):
            session['userE'] = checkT.username
            return redirect("/dashboard")
        else:
            return redirect("/signin")

    return render_template('verify.html')


@app.route("/logout")
def logout():
    if 'user' in session:
        session.pop('user', None)  # Remove 'user' from the session
    if 'userE' in session:
        session.pop('userE', None)  # Remove 'userE' from the session
    return redirect('/signin')

app.run(debug=True)



