# -*- coding: utf-8 -*-
import random
from datetime import datetime
import string
from flask_bootstrap import Bootstrap
from uploader import save_file
from forms import LoginForm, RegisterForm, AsignForm
from flask_login import LoginManager, login_user, login_required, logout_user
from flask import Flask, \
    request, \
    render_template, \
    flash, \
    session as login_session, \
    url_for, \
    redirect
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker, scoped_session
from modules import Base, User, Device, DeviceEmployee, Issue
app = Flask(__name__)
Bootstrap(app)
engine = create_engine('sqlite:///DataStore.db')
Base.metadata.bind = engine
session = scoped_session(sessionmaker(bind=engine))
login_Manager = LoginManager()
login_Manager.init_app(app)
login_Manager.login_view = 'login'


@app.route('/')
@app.route('/index')
@login_required
def index():
    if login_session['type'] == 'EMPLOYEE':
        oreders = get_Tasks()
        return render_template('index.html', orders=oreders)
    if login_session['type'] == 'ADMIN':
        orders = session.query(DeviceEmployee).filter(
            or_(DeviceEmployee.issues == 1,DeviceEmployee.status == 1)).all()
        devices = session.query(Device).all()
    return render_template('index.html', orders=orders, devices=devices)


@app.route('/orders/<int:order_id>/delete', methods={"GET", "POST"})
@login_required
def delete_order(order_id):
    if login_session['type'] != 'ADMIN':
        flash('You Not Authorized To Access This Page')
        return redirect(url_for('index'))
    order = session.query(DeviceEmployee).filter_by(id=order_id).first()
    print "this is Order:"
    print order
    if not order:
        print "this is Order:"
        return render_template('404.html'),404
    if request.method == 'POST':
        session.delete(order)
        session.commit()
        flash('Item Deleted Succssfully')
        return redirect(url_for('index'))
    return render_template('deleteOrder.html', order=order)

@app.route('/orders/<int:order_id>', methods={"GET", "POST"})
@login_required
def show_order(order_id):
    order = session.query(DeviceEmployee).filter_by(id=order_id).first()
    if not order:
        return render_template('404.html'), 404
    elif order.user_id != login_session['id']:
        flash("you not Authorized to access this")
        return redirect(url_for('index'))
    if request.method == 'POST':
        status =request.form['status']
        if status and status == "True":
            order.status = True
            order.device.quantity -= 1
            if request.form['Add']:
                order.addtion = request.form['Add']
        elif status and status == "False":
            order.status = False
            order.issues = True
            message = request.form['cancelationReason']
            if not message:
                flash('Please Enter reason of cancellation')
                return redirect(request.url)
            order.message = message
        session.commit()
        flash("Response Sended")
        return redirect(url_for('index'))
    return render_template('viewOrder.html', item=order)



@app.route('/AssignDevice', methods={"GET", "POST"})
@login_required
def assign_device():
    if login_session['type'] != 'ADMIN':
        flash('You Not Authorized To Access This Page')
        return redirect(url_for('index'))
    devices = session.query(Device).all()
    devices_filtered =[]
    for device in devices:
        if device.quantity > 0:
            devices_filtered.append(device)
    form = AsignForm(request.form)
    users = session.query(User).filter_by(type='EMPLOYEE').all()
    if not devices_filtered:
        flash('Please Add Device First')
        return redirect(url_for('index'))
    if not users:
        flash('Please Add Employee First')
        return redirect(url_for('index'))
    form.Device.choices = [(g.id, g.name) for g in devices_filtered]
    form.user.choices = [(g.id, g.name) for g in users]
    if request.method == 'POST':
        print 'TESTing'
        print(form.Device.data)
        if form.is_submitted() and form.validate():
            time = request.form['time']
            date = request.form['date']

            if not (time and date):
                flash("please Choice  The Time and Day")
                return redirect(request.url)
            date += ' ' + time
            py_date = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order = DeviceEmployee(user_id=form.user.data, client_name=form.clientName.data,
                                   time=py_date, address=form.Address.data, device_id=form.Device.data,
                                   phone=form.PhoneNumber.data)
            session.add(order)
            session.commit()
            flash('This Task Assigned To %s' % form.user.data)
            return redirect(url_for('index'))

    return render_template('AsignDevice.html', form=form)


@app.route('/newDevice', methods={"POST", "GET"})
@login_required
def new_device():
    if login_session['type'] != 'ADMIN':
        flash('You Not Authorized To Access This Page')
        return redirect(url_for('index'))
    if request.method == "POST":
        name = request.form['name']
        number = request.form['number']
        # Add New Category
        if name and number and not name.isspace():
            try:
                number = int(number)
                if number > 0:
                    device = Device(name=name, quantity=number)
                    session.add(device)
                    session.commit()
                else:
                    flash("Number of Device Cant Be less Than 1")
                    return redirect(request.url)
            except Exception:
                flash('ERROR Plese Try Again')
            flash("Device %s Added " % device.name)
            return redirect(url_for('index'))
        # the Field of name is empty
        else:
            flash("All Items Needed")
            return render_template("NewDevice.html")
    return render_template('NewDevice.html')


# login and authentication Function
@login_Manager.user_loader
def load_user(user_id):
    return session.query(User).filter_by(id=int(user_id)).one_or_none()


@app.route('/login', methods={"GET", "POST"})
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            user = session.query(User).filter(
                or_(User.username == form.username.data, User.email == form.username.data)).one_or_none()
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


@app.route('/AddnewUser', methods={"GET", "POST"})
@login_required
def add_user():
    if login_session['type'] != 'ADMIN':
        flash('You Not Authorized To Access This Page')
        return redirect(url_for('index'))
    form = RegisterForm(request.form)
    print 'this is user ID :LPL'
    if request.method == "POST":
        if form.validate_on_submit():
            print 'this is user ID :'
            username = session.query(User) \
                .filter(User.username == form.username.data).one_or_none()
            if username:
                flash('The username Used Before')
                return redirect(request.url)
            user_email = session.query(User) \
                .filter(User.email == form.email.data).one_or_none()
            if user_email:
                flash('This Email Used Before')
                return redirect(request.url)
            # all Ok saving  User
            user = User(name=form.name.data, email=form.email.data,
                        username=form.username.data, type=form.type.data)
            user.hash_password(form.password.data)
            session.add(user)
            session.flush()
            if request.files['file']:
                filename = save_file(request.files['file'], str(user.id))
                if filename:  # Check if the photo is saved or not
                    user.picture = u'users/' + filename
                else:  # error in saving the photo
                    flash("This Isn't an Image")
                    return redirect(request.url)
            else:
                session.commit()
                flash("Employee %s Added Successfully"%user.name)
                return redirect(url_for('index'))

    return render_template('addUser.html', form=form)


# logout
@app.route('/logout')
def logout():
    logout_user()
    del login_session['username']
    del login_session['id']
    del login_session['email']
    flash("You have successfully been logged out.")
    return redirect(url_for('index'))


#EMployee
def get_Tasks():
    return session.query(DeviceEmployee).filter_by(user_id=login_session['id'], status=0,issues=0).all()


# if user enter wrong url
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', e=e), 404


if __name__ == "__main__":
    app.secret_key = "Bl7a & Not"
    app.debug = True
    app.run(port=5000, threaded=True)
