from flask import Flask, render_template, request,flash,redirect,url_for,session,logging
from wtforms import Form,StringField,TextAreaField,PasswordField,validators,ValidationError
from passlib.hash import sha256_crypt
from functools import wraps
from keras.models import model_from_json
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import os, coin_data, pickle, sys
from flask_mysqldb import MySQL



app = Flask('crypto_predictor')

#Secret Key is used for using Flash Messages
app.secret_key= "crypto_predictor"

#MySQL DB connection
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] ="crypto_predictor"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)



#Regiser Form Attributes
class RegisterForm(Form):
    name = TextAreaField("Name & Surname",validators=[validators.Length(min=4,max=25),validators.DataRequired()])
    username = StringField('Username',validators=[validators.Length(min=5,max=35),validators.DataRequired()])
    email = StringField('Email Address',validators= [validators.Email(message ="Please enter an valid email address!")])
    password = PasswordField('Password', validators=[
        validators.DataRequired(message="Please set a password"),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    

    
class LoginForm(Form):
    username = StringField("Username")
    password = PasswordField("Password")


#Model and Weights Loading
sc = MinMaxScaler()
json_file = open('model_1h.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("model_1h.h5")
print("Loaded model from disk")


def model_compiling(loaded_model):
    loaded_model.compile(optimizer="adam", loss="mse")
    return loaded_model


#Dataframe Manuplation for unnecessary parts.
new_df = pd.read_csv('Binance_BTCUSDT_1h.csv')
df = new_df.drop(['unix', 'date', 'symbol', 'open', 'high', 'low', 'Volume BTC', 'Volume USDT', 'tradecount'], axis=1)
#Fitting the model
df = sc.fit_transform(df)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/about')
def about():
    return render_template('about.html')


#Login Page
@app.route('/login',methods = ["GET","POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        #Firstly, we need to get the data comes from user
        username = form.username.data
        password_entered = form.password.data
        
        #Generating cursor
        cursor = mysql.connection.cursor()

        query = "Select * From users where username = %s"

        #Do not forget put a comma because if we don't, 
        #function can't understand that it is a tuple
        result = cursor.execute(query, (username,))
        
        # result =0 means that there is no such a user with that username
        # result = 1 means that there is a user with that name. 
        # We need to query the passwords
        if result > 0:
            data = cursor.fetchone()

            # Here actually real password is in encrypted form
            real_password = data["password"]
            
            # We examine whether the entered and real password is matched 
            if sha256_crypt.verify(password_entered, real_password):
                flash("You signed in successfully!", "success")
                return redirect(url_for("index"))
            else:
                flash("You entered your passwod incorrectly...", "danger")
                return redirect(url_for("login"))
                
            
        else:
            flash("There is no such user!", "danger")
            return redirect(url_for("login"))




    return render_template('login.html',form=form)


#Register Page
@app.route("/register",methods = ["GET","POST"])
def register():
    #Form request initialization 
    form = RegisterForm(request.form)

    if request.method == "POST" and form.validate():
        
        #We need to get the attributes and data from our form
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)

        #Generating cursor for db operations
        cursor = mysql.connection.cursor()
        
        #We add respectively
        query = "Insert into users(name,email,username,password) VALUES(%s,%s,%s,%s)"
        
        #Query operation with cursor execution
        cursor.execute(query,(name,email,username,password))
        
        #Changing in DB should be committed (Like Git push)
        mysql.connection.commit()

        #For avoiding unnecessary source usage, wen need to close cursor.
        cursor.close()
        
        flash("Congratulations! You have signed up successfully!","success")
        
        session["logged_in"] = True
        session["username"] = username
 
        return redirect(url_for("login"))
    else:
        return render_template("register.html",form = form)

@app.route('/logout')
def logout():
    #We need to clear the session at the beggining of logout function
    session.clear()
    return redirect(url_for("index"))



#Predictions Page. Importing pre-trained model and current prices
@app.route('/predictions')
def results():
    model = model_compiling(loaded_model)
    price = float(coin_data.current_btc_usd_price())
    scaled_price = sc.transform([[price]])
    predicted_price = float(model.predict(scaled_price))
    if predicted_price > price:
        advice = "BUY"
        statement = 1
    else:
        advice = "SELL"
        statement = 0
    return render_template('predictions.html', price=price, predicted_price=predicted_price,advice=advice,statement=statement)


if __name__ == '__main__':
    app.run(debug=False, host='localhost')