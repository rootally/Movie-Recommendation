from flask import Flask, render_template, request, redirect, url_for, session
from flask_mongoengine import MongoEngine, Document
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import Email, Length, InputRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
#from flask.ext.pymongo import PyMongo
import pandas as pd

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'movie_r',
    'host': 'mongodb://root:root1234@ds127115.mlab.com:27115/movie_r'
}

class movie(object):

    def __init__(self,movie_id,name,year,director,rating):
        self.movie_id=movie_id
        self.name=name
        self.year=year
        self.director=director
        self.rating=rating

db = MongoEngine(app)
print(db)
app.config['SECRET_KEY'] = '_5#y2L"F4Q8z\n\xec]/'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Ratings(db.EmbeddedDocument):
   rating = db.IntField(default=0)


class User(UserMixin, db.Document):
    meta = {'collection': 'users'}
    email = db.StringField(max_length=30)
    password = db.StringField()
    content = db.ListField(db.EmbeddedDocumentField(Ratings))


@login_manager.user_loader
def load_user(user_id):
    print (User.objects(pk=user_id).first())
    return User.objects(pk=user_id).first()

class RegForm(FlaskForm):
    email = StringField('email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=1, max=20)])
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    print()
    form = RegForm()
    if request.method == 'POST':
        if form.validate():
            print(form.email.data)
            existing_user = User.objects(email=form.email.data).first()
            #print(existing_user)
            if existing_user is None:
                hashpass = generate_password_hash(form.password.data, method='sha256')
                fd = pd.read_csv('data.csv',names=["movie_id","movie_name","year","director", "rating"])
                hey = User(form.email.data,hashpass).save()
                for i in fd['movie_id']:
                    rat = Ratings()
                    hey.content.append(rat)
                hey.save()                
                login_user(hey)
                return redirect(url_for('dashboard'))
    return render_template('register.html', form=form)

@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated == True:
        return redirect(url_for('dashboard'))
    form = RegForm()
    if request.method == 'POST':
        if form.validate():
            check_user = User.objects(email=form.email.data).first()
            if check_user:
                if check_password_hash(check_user['password'], form.password.data):
                    login_user(check_user)
                    session['username'] = form.email.data
                    return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    fd=pd.read_csv("data.csv", names=["movie_id","movie_name","year","director", "rating"])
    data_dict=fd.to_dict()
    movie_list=[]
    for i in range(len(fd)):
        movie_list.append(movie(fd.loc[i,"movie_id"],fd.loc[i,"movie_name"],fd.loc[i,"year"],fd.loc[i,"director"],fd.loc[i,"rating"]))
    #print(x.movie_id)
    return render_template('dashboard.html', name=current_user.email, movieList=movie_list)

@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/analyse', methods = ['POST','GET'])
def analyse():
    data = request.form
    curUser = User.objects(email=session['username']).first()
    print(curUser.password)
    print(session['username'])
    fd = pd.read_csv('data.csv',names=["movie_id","movie_name","year","director", "rating"])
    for key,val in data.items():
        if val!='' and val!='submit':
            for i,j in enumerate(fd['movie_id']):
                if int(j)==int(key):
                    curUser.content[i].rating = int(val)
    curUser.save()
    row = []
    col = []
    for i in  User.objects:
        for j in i.content:
            col.append(j.rating)
        row.append(col)
        col = []
    #print(row)
    df = pd.DataFrame(row,columns=[v for v in fd['movie_id']])
    df.to_csv('tst.csv')
    return render_template('dashboard.html')

# @app.route("/")
# def index():
#     if current_user.is_authenticated == True:
#         return redirect(url_for('dashboard'))
#     form = RegForm()
#     if request.method == 'GET':
#         if form.validate():
#             check_user = User.objects(email=form.email.data).first()
#             if check_user:
#                 if check_password_hash(check_user['password'], form.password.data):
#                     login_user(check_user)
#                     return redirect(url_for('dashboard'))
#     return render_template('index.html',form=form)

if __name__ == "__main__":
	app.run(debug=True)
