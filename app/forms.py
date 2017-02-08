from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, validators,PasswordField,BooleanField,StringField
from wtforms.validators import DataRequired
import datetime

class RegistrationForm(FlaskForm):
    imgPath = StringField('image path')
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Services', [validators.DataRequired()])

class RemovingForm(FlaskForm):
    accept_removing = BooleanField('I accept removing my account', [validators.DataRequired()])

class FindAccountForm(FlaskForm):
    fusername = StringField('Username', [validators.Length(min=4, max=25)])
    femail = StringField('Email Address', [validators.Length(min=6, max=35)])


class editForm(FlaskForm):
    imgPath = StringField('image path')
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

class PostingForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    content = TextAreaField('content', validators=[DataRequired()])
    imgPath = StringField('image path')
