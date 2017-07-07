from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length


class LoginForm(FlaskForm):
    username = StringField('Username OR Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember me')


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=4, max=30)])
    username =StringField('username', validators=[InputRequired(), Length(min=4, max=30)])
    email = StringField('Email', validators=[InputRequired(), Length(min=4, max=30),
                                             Email(message="Please Enter valide Email")])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])


class AsignForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=4, max=30)])
    email = StringField('Email', validators=[InputRequired(), Length(min=4, max=30),
                                             Email(message="Please Enter valide Email")])
