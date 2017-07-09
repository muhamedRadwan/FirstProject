# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, validators, SelectField,DateTimeField
from wtforms.validators import InputRequired, Email, Length


class LoginForm(FlaskForm):
    username = StringField('Username OR Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember me')


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=4, max=30)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=30)])
    email = StringField('Email', validators=[InputRequired(), Length(min=4, max=30),
                        Email(message="Please Enter valide Email")])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80),
                                                     validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    type = SelectField(u'Type', choices=[('EMPLOYEE', 'Employee'), ('ADMIN', 'Admin')])


class AsignForm(FlaskForm):
    clientName = StringField(u'أسم العميل', validators=[InputRequired(), Length(min=4, max=50)])
    PhoneNumber = StringField(u'رقم العميل', validators=[InputRequired(), Length(min=4, max=30)])
    Address = StringField(u'الموقع', validators=[InputRequired(), Length(min=4, max=300)])
    Device = SelectField(u'نوع الجهاز', coerce=int, validators=[validators.optional()])
    user = SelectField(u'username العامل', coerce=int, validators=[validators.optional()])
