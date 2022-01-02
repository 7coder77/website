from flask import *
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dao.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['SECRET_KEY'] = 'the random string'  
db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    msg = db.Column(db.String(1000),  nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    passwd = db.Column(db.String(120), nullable=False)
    Gender = db.Column(db.String(1), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/Cuslog", methods=['GET','POST'])
def customer_login():
    if(request.method == "POST"):
        email=request.form.get("email")
        password=request.form.get("passwd")
        q=User.query.filter_by(email=email).first()
        if(q and q.passwd==password):
            return"Welcome"
        else:
            flash("*Incorrect Email or Password")
            return redirect(url_for("customer_login"))
    else:
        return render_template("customer_login.html")


@app.route("/adlog", methods=['GET','POST'])
def admin_login():
    if(request.method=='POST'):
        email=request.form.get("email")
        password=request.form.get("pass")
        if(email== "ADMIN" and password == "adpassword"):
            session["admin"] = email
            return render_template("adsuc.html",uname=session['admin'])
        else:
            flash("*Incorrect Email or Password")
            return redirect(url_for("admin_login"))
    return render_template("admin_login.html")


@app.route("/contact", methods=['GET','POST'])
def contact():
    if (request.method=='POST'):
        name=request.form.get("name")
        email=request.form.get("email")
        msg=request.form.get("msg")
        query=Contact(name=name,email=email,msg=msg)
        db.session.add(query)
        db.session.commit()
        flash("Your message is send to admin panel you will be notified soon")
        return redirect(url_for("home"))
    else:
        return render_template("contact.html")


@app.route("/notcontact")
def fetch_contact():
    if not session.get("admin"):
      return render_template("illegal.html")  
    data=Contact.query.all()
    print(data)
    return render_template("viewdata.html",data=data)


@app.route("/logout/<sess>")
def logout(sess):
    if sess=="ADMIN":
        new="admin"
        session.pop(new , None)
    else:
        session.pop(sess, None)
    return redirect(url_for('home'))


@app.route("/adduser",methods=["GET","POST"])
def adduser():
    if (request.method=='POST'):
        name=request.form.get("name")
        email=request.form.get("email")
        passwd=request.form.get("passwd")
        gender=request.form.get("gender")
        age=request.form.get("age")
        q=User(name=name,email=email,passwd=passwd,Gender=gender,age=age)
        db.session.add(q)
        db.session.commit()
        flash("New user added successfully")
        return render_template("adsuc.html")

    else:
        if not session.get("admin"):
            return render_template("illegal.html")
        return render_template("add_user.html") 

if __name__=="__main__":
    app.run(debug=True)