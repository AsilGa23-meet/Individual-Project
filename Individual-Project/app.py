from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here
config = {
  "apiKey": "AIzaSyDvZ9o19c0oQOwSl4faMG9YctRtiKFF3jI",
  "authDomain": "personal-24e1c.firebaseapp.com",
  "projectId": "personal-24e1c",
  "storageBucket": "personal-24e1c.appspot.com",
  "messagingSenderId": "236072160472",
  "appId": "1:236072160472:web:12a318e7515ee41dd15bad",
  "measurementId": "G-M6ENR0BF9Y",
  "databaseURL":"https://personal-24e1c-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('sweet_home'))
        except:
            error = "Authentication failed"
            return error
    return render_template("Signin.html")

@app.route('/signup',  methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        repeat_password = request.form['password-repeat']
        if email == "asilllimar@gmail.com" and password == "asil123":
            db.child("Users").child(login_session).get().val()["admin"] = True
        else:
            admin = False
        if password == repeat_password:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user = {"name": name,"password":password,"email": email, "admin":admin, "points":0}
            db.child("Users").child(login_session['user']['localId']).set(user)
            return redirect('/home')
        else:
            return render_template("Signup.html")
    return render_template("Signup.html")


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    points = db.child("Users").child(login_session['user']['localId']).child("points").get().val()
    return render_template("profile.html" ,points=points)


@app.route('/signout', methods=['GET', 'POST'])
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect('/')



@app.route('/home', methods=['GET', 'POST'])
def sweet_home():
    return render_template("index.html")

@app.route('/input', methods=['GET', 'POST'])
def add():
    user = db.child("Users").child(login_session['user']['localId']).get().val()
    points = user['points']

    if request.method=='POST':
        points = request.form['points']
        return render_template("inputt.html",points=points)
    return render_template("inputt.html" ,points=points)

#<string:name>



#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)