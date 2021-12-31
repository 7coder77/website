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


@app.route("/Cuslog")
def customer_login():
    return render_template("customer_login.html")


@app.route("/adlog", methods=['GET','POST'])
def admin_login():
    if(request.method=='POST'):
        email=request.form.get("email")
        password=request.form.get("pass")
        if(email== "ADMIN" and password == "adpassword"):
            session["admin"] = email
            return render_template("adsuc.html",uname=session['admin'])
    return render_template("admin_login.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/cdetail", methods=['GET','POST'])
def contact_return():
    if (request.method=='POST'):
        name=request.form.get("name")
        email=request.form.get("email")
        msg=request.form.get("msg")
        query=Contact(name=name,email=email,msg=msg)
        db.session.add(query)
        db.session.commit()
        return "submit done"
    else:
        return redirect(url_for('home'))


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

if __name__=="__main__":
    app.run(debug=True)