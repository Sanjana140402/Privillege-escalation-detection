from flask import Flask,request, url_for, redirect, render_template
import pandas as pd
import numpy as np
import joblib
import sqlite3
import pickle



model = joblib.load(r'model.sav')
cv = pickle.load(open('tf.pkl', 'rb'))

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route('/login')
def login():
	return render_template('signin.html')

@app.route('/logon')
def logon():
	return render_template('signup.html')

@app.route("/signup")
def signup():
    
    
    name = request.args.get('username','')
    number = request.args.get('number','')
    email = request.args.get('email','')
    password = request.args.get('password','')

    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("insert into `detail` (`name`,`number`,`email`, `password`) VALUES (?, ?, ?, ?)",(name,number,email,password))
    con.commit()
    con.close()

    return render_template("signin.html")

@app.route("/signin")
def signin():

    mail1 = request.args.get('user','')
    password1 = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("select `name`, `password` from detail where `name` = ? AND `password` = ?",(mail1,password1,))
    data = cur.fetchone()

    if data == None:
        return render_template("signin.html")    

    elif mail1 == 'admin' and password1 == 'admin':
        return render_template("index.html")

    elif mail1 == str(data[0]) and password1 == str(data[1]):
        return render_template("index.html")
    else:
        return render_template("signin.html")

@app.route('/index')
def index():
   return render_template('index.html')



@app.route('/notebook')
def notebook():
	return render_template('notebook.html')


@app.route('/predict1', methods=['POST'])
def predict1():
    if request.method == 'POST':
        message = request.form['message']
        data = [message]
        vectorizer = cv.transform(data).toarray()
        prediction = model.predict_proba(vectorizer)
        print(prediction)
        output = '{0:.{1}f}'.format(prediction[0][1], 2)
        print(output)
        if output > str(1.00):
            return render_template('result.html',pred=f'Insider threat detected')
        else:
            return render_template('result.html',pred=f'You are safe')
        




if __name__ == '__main__':
   app.run()