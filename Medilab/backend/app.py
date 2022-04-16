
import email
from enum import unique
from operator import index

from pickle import dump
from flask import Flask,render_template,request,redirect,flash
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PrimaryKeyConstraint, Table, select, true
from flask_login import UserMixin
from flask_login import login_required,logout_user,login_user,login_manager,LoginManager,current_user



#my database connection
local_server = True
app = Flask(__name__)
app.secret_key = "prem"


#unique user access
#login_manager = LoginManager(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"

# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql:///username:password@localhost/databasename"

#app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@127.0.0.2:3307/medserv"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://wqyhnamgjagypy:eecc88a24bbdecfcdca88fd04e8546e7700c3b81b44d741fbb539dbe753c23ee@ec2-34-194-158-176.compute-1.amazonaws.com:5432/dfk39eri6aqujp"
db = SQLAlchemy(app) 


dl  = "nan"

@login_manager.user_loader
def load_user(user_id):
    if dl == "Doctor":
        return Doctor.query.get(int(user_id))
    elif dl == "User":
        return User.query.get(int(user_id))


class Test( db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.column(db.String(50))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    uname = db.Column(db.String(25))
    umail = db.Column(db.String(25), unique=True)
    uphone = db.Column(db.String(14), unique=True)
    udob = db.Column(db.String(25))
    ugender = db.Column(db.String(10))
    auphone = db.Column(db.String(14))
    upass =  db.Column(db.String(30))
    cupass =  db.Column(db.String(30))
    upin = db.Column(db.Integer)
    ucaddress =  db.Column(db.String(60))
    upaddress =  db.Column(db.String(60))

# id																		

class Doctor(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    dname = db.Column(db.String(50))
    dmail = db.Column(db.String(100), unique=True)
    dphone = db.Column(db.String(15), unique=True)
    ddob = db.Column(db.String(100))
    dgender = db.Column(db.String(50))
    adphone = db.Column(db.String(100))
    daa = db.Column(db.String(19))
    dcs = db.Column(db.String(200))
    dgu = db.Column(db.String(100))
    dyog = db.Column(db.Integer)
    dus = db.Column(db.String(100))
    duprn = db.Column(db.String(100), unique=True)
    dpass =  db.Column(db.String(100))
    cdpass =  db.Column(db.String(100))
    dfile = db.Column(db.Text)
    dcaddress =  db.Column(db.String(100))
    dpaddress =  db.Column(db.String(100))

class Userdata(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), primary_key = True, index_key = True)
    udis = db.Column(db.String(100))
    utd = db.Column(db.String(20))
    uhc = db.Column(db.String(100))
    udocn = db.Column(db.String(100))   								
    udloc =  db.Column(db.String(100))
    udcon =  db.Column(db.String(15))
    umed =  db.Column(db.String(100))

class Doctordata(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100))
    uname = db.Column(db.String(100))
    udis = db.Column(db.String(100))
    utd = db.Column(db.String(100))
    uhc = db.Column(db.String(100))
    udocn = db.Column(db.String(100))   								
    udloc =  db.Column(db.String(100))
    udcon =  db.Column(db.String(100), primary_key = True, index_key = True)
    umed =  db.Column(db.String(100))
    


@app.route("/", methods=['POST','GET'])
def home():
    results = User.query.filter(User.id).all()
    results2 = Doctor.query.filter(Doctor.id).all()
    total1 = len(results) 
    total2 = len(results2)
    listsk =[]
    listsk.append(total1)
    listsk.append(total2)

    return render_template("index.html", postsdata=listsk)



# @app.route("/usersignup")
# def usersignup():
#     return render_template("usersignup.html")


# @app.route("/userlogin")
# def userlogin():
#     return render_template("userlogin.html")



@app.route("/signup", methods=['POST','GET'])
def signup():
    if request.method == "POST":
        funame = request.form.get('uname') 
        fumail = request.form.get('umail')
        fudob = request.form.get('udob')

        fugender = request.form.get('ugender')
        fuphone = request.form.get('uphone')
        fauphone = request.form.get('auphone')
        fupass = request.form.get('upass')
        fcupass = request.form.get('cupass')
        fupin = request.form.get('upin')
        fucaddress = request.form.get('ucaddress')
        fupaddress = request.form.get('upaddress')
        funame = request.form.get('uname')
        
        user = User.query.filter_by(umail = fumail).first()
        phcheck = User.query.filter_by(uphone = fuphone).first()
        if user or phcheck:
            flash("E-mail or Phone You have entered Already Exist", "info")
            return render_template("usersignup.html")

        new_user = db.engine.execute(f"INSERT INTO `user` (`id`, `uname`, `umail`, `uphone`, `udob`, `ugender`, `auphone`, `upass`, `cupass`, `upin`, `ucaddress`, `upaddress`)  VALUES (NULL, '{funame}','{fumail}','{fuphone}','{fudob}','{fugender}','{fauphone}','{fupass}','{fcupass}','{fupin}','{fucaddress}','{fupaddress}');")

        flash("Registration Successful enter Credential for Account Access", "success")
        
        return render_template("userlogin.html")
        
    return render_template("usersignup.html")



@app.route("/login", methods=['POST','GET'])
def login():
    if request.method == "POST":
        global dl
        email = request.form.get('ulmail') 
        upass = request.form.get('ulpass')
        dl  = request.form.get('ulabel')
        user = User.query.filter_by(umail = email).first_or_404(description='There is no data with {}'.format(email))

        if user and user.upass == upass:

            login_user(user)
            postsdata = Userdata.query.filter_by(email = email).all()
            flash("Login Successful", "success")
            return render_template("cusers.html", postsdata=postsdata)
        else:
            flash("Invalid Credential", "danger")
            return render_template("userlogin.html")
        
    return render_template("userlogin.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout Successful","warning")
    return redirect(url_for('login'))

@app.route('/doclogout')
@login_required
def doclogout():
    logout_user()
    
    flash("Logout Successful","warning")
    return redirect(url_for('doctorlogin'))



@app.route("/test")
def test():
    try:
        a = Test.query.all()
        print(a)
        return "My databse is connected"
    except Exception as e:
        print(e)
        return "database isnot connected"


@app.route("/userdash")
@login_required
def userdash():
    email = current_user.umail
    postsdata = Userdata.query.filter_by(email = email).all()
    return render_template("cusers.html", postsdata=postsdata)

# @app.route("/cusers")
# @login_required
# def cusers():
#     return render_template("cuserdash.html")




@app.route("/cusers", methods=['POST','GET'])
@login_required
def cusers():
    email = current_user.umail
    # postsdata = Userdata.query.filter_by(email = email).first_or_404(description='There is no data with {}'.format(email))
    postsdata = Userdata.query.filter_by(email = email).all()
    if request.method == "POST":
        fumail = request.form.get('email')
        funame = request.form.get('uname')
        fudis = request.form.get('udis') 
        futd = request.form.get('utd')
        fuhc = request.form.get('uhc')
        fudocn = request.form.get('udocn')
        fudloc = request.form.get('udloc')
        fudcon = request.form.get('udcon')
        fumed = request.form.get('umed')
        
        # user = User.query.filter_by(umail = fumail).first()
        # phcheck = User.query.filter_by(uphone = fuphone).first()
        # if user or phcheck:
        #     flash("E-mail or Phone You have entered Already Exist", "info")
        #     return render_template("usersignup.html")
        							
        new_user = db.engine.execute(f"INSERT INTO `userdata` (`id`, `email`, `uname`, `udis`, `utd`, `uhc`, `udocn`, `udloc`, `udcon`, `umed`)  VALUES (NULL, '{fumail}', '{funame}','{fudis}','{futd}','{fuhc}','{fudocn}','{fudloc}','{fudcon}','{fumed}');")

        flash("Data Added Succesfully", "success")
        
        return render_template("cuserdash.html",postsdata=postsdata)
        
    return render_template("cuserdash.html",postsdata=postsdata)

@app.route("/emergency")
@login_required
def emergency():
    return render_template("emergency.html")



@app.route("/doctorsignup", methods=['POST','GET'])
def doctorsignup():
    if request.method == "POST":
        fdname = request.form.get('dname') 
        fdmail = request.form.get('dmail')
        fdphone = request.form.get('dphone')
        fddob = request.form.get('ddob')
        fdgender = request.form.get('dgender')
        fadphone = request.form.get('adphone')
        fdaa = request.form.get('daa') 
        fdcs = request.form.get('dcs')
        fdgu = request.form.get('dgu')
        fdyog = request.form.get('dyog') 
        fdus = request.form.get('dus')
        fduprn = request.form.get('duprn')
        fdpass = request.form.get('dpass')
        fcdpass = request.form.get('cdpass')
        fdfile = request.form.get('dfile')
        fdcaddress = request.form.get('dcaddress')
        fdpaddress = request.form.get('dpaddress')
    
        
        doctor = Doctor.query.filter_by(dmail = fdmail).first()
        phcheck = Doctor.query.filter_by(dphone = fdphone).first()
        if doctor or phcheck:
            flash("E-mail or Phone You have entered Already Exist", "info")
            return render_template("doctorsignup.html")

        new_user = db.engine.execute(f"INSERT INTO `doctor` (`id`, `dname`, `dmail`, `dphone`, `ddob`, `dgender`, `adphone`, `daa`, `dcs`, `dgu`, `dyog`, `dus`, `duprn`, `dpass`, `cdpass`, `dfile`, `dcaddress`, `dpaddress`)  VALUES (NULL, '{fdname}','{fdmail}','{fdphone}','{fddob}','{fdgender}','{fadphone}', '{fdaa}','{fdcs}','{fdgu}','{fdyog}','{fdus}','{fduprn}','{fdpass}','{fcdpass}','{fdfile}','{fdcaddress}','{fdpaddress}');")

        flash("Registration Successful enter Credential for Account Access", "success")
        return render_template("doctorlogin.html")
        
    return render_template("doctorsignup.html")

@app.route("/doctorlogin", methods=['POST','GET'])
def doctorlogin():
    if request.method == "POST":
        global dl
        email = request.form.get('dlmail') 
        upass = request.form.get('dlpass')
        uprn = request.form.get('dluprn')
        dl = request.form.get('dlabel')
        user = Doctor.query.filter_by(dmail = email).first_or_404(description='There is no data with {}'.format(email))

        # print(dl)

        if user and user.dpass == upass and user.duprn==uprn:
            
            login_user(user)

            postsdata = Doctordata.query.filter_by(udcon = email).all()
            flash("Login Successful", "success")
            return render_template("docdash.html",postsdata=postsdata)
        else:
            flash("Invalid Credential", "danger")
            return render_template("doctorlogin.html")
        
    return render_template("doctorlogin.html")

@app.route("/dash")
@login_required
def dash():
    # print("found : ", dl)
    email = current_user.dmail
    postsdata = Doctordata.query.filter_by(udcon = email).all()
    return render_template("docdash.html",postsdata=postsdata)

@app.route("/docp", methods=['POST','GET'])
@login_required
def docp():
    email = current_user.dmail
    # postsdata = Userdata.query.filter_by(email = email).first_or_404(description='There is no data with {}'.format(email))
    postsdata = Doctordata.query.filter_by(udcon = email).all()
    if request.method == "POST":
        fumail = request.form.get('email')
        funame = request.form.get('uname')
        fudis = request.form.get('udis') 
        futd = request.form.get('utd')
        fuhc = request.form.get('uhc')
        fudocn = request.form.get('udocn')
        fudloc = request.form.get('udloc')
        fudcon = request.form.get('udcon')
        fumed = request.form.get('umed')
        
        # user = User.query.filter_by(umail = fumail).first()
        # phcheck = User.query.filter_by(uphone = fuphone).first()
        # if user or phcheck:
        #     flash("E-mail or Phone You have entered Already Exist", "info")
        #     return render_template("usersignup.html")
        							
        new_user = db.engine.execute(f"INSERT INTO `doctordata` (`id`, `email`, `uname`,`udis`, `utd`, `uhc`, `udocn`, `udloc`, `udcon`, `umed`)  VALUES (NULL, '{fumail}','{funame}','{fudis}','{futd}','{fuhc}','{fudocn}','{fudloc}','{fudcon}','{fumed}');")

        new_user2 = db.engine.execute(f"INSERT INTO `userdata` (`id`, `email`, `uname`,`udis`, `utd`, `uhc`, `udocn`, `udloc`, `udcon`, `umed`)  VALUES (NULL, '{fumail}','{funame}','{fudis}','{futd}','{fuhc}','{fudocn}','{fudloc}','{fudcon}','{fumed}');")

        flash("Data Added Succesfully", "success")
        
        return render_template("docpatients.html",postsdata=postsdata)
    return render_template("docpatients.html",postsdata=postsdata)







app.run(debug = True)