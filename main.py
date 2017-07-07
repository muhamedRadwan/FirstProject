import random
import string
from flask_bootstrap import Bootstrap
from uploader import save_file
from forms import LoginForm, RegisterForm, AsignForm
from flask_login import LoginManager, login_user, login_required, logout_user
from flask import Flask,\
    jsonify,\
    request,\
    render_template,\
    flash,\
    session as login_session,\
    url_for,\
    make_response,\
    redirect
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from modules import Base, User, Device, DeviceEmployee, Issue
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import json
import httplib2
import requests
app = Flask(__name__)
Bootstrap(app)



engine = create_engine('sqlite:///DataStore.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
login_Manager = LoginManager()
login_Manager.init_app(app)
login_Manager.login_view = 'login'



@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')


# login and authentication Function
@login_Manager.user_loader
def load_user(user_id):
    return session.query(User).filter_by(id=int(user_id)).one_or_none()


@app.route('/login', methods={"GET", "POST"})
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            user = session.query(User).filter(or_(User.username == form.username.data, User.email == form.username.data)).one_or_none()
            if not user or user.password_hash is None or not user.verify_password(form.password.data):
                flash('Error Unknown Username Or Password ')
                return redirect(request.url)
            else:
                login_session['id'] = user.id
                login_session['username'] = user.name
                login_session['email'] = user.email
                login_session['picture'] = user.picture
                login_session['provider'] = 'website'
                login_session['type'] = user.type
                login_user(user, remember=form.remember.data)
                return redirect(url_for('index'))
    state = ''.join(random.choice(string.uppercase + string.digits) for i in xrange(32))
    login_session['state'] = state
    return render_template('loginTest.html', STATE=state, form=form)

# logout
@app.route('/logout')
def logout():
    logout_user()
    del login_session['username']
    del login_session['id']
    del login_session['email']
    flash("You have successfully been logged out.")
    return redirect(url_for('index'))


# if user enter wrong url
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', e=e), 404

if __name__ == "__main__":
    app.secret_key = "Bl7a & Not"
    app.debug = True
    app.run(port=5000)