# Importações de extensões Flask
from flask_wtf import FlaskForm

# Importações do WTForms
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField, ValidationError, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length

# Importações do seu projeto
from app.models.models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message='Email is required'), Email()])
    password = PasswordField('Password', validators=[DataRequired(message='Password is required'), Length(min=6)])
    errors = HiddenField("Errors")
    submit = SubmitField('Login')
    valid = True

class RegistrationForm(FlaskForm):
    name = StringField('First Name', validators=[DataRequired(message='First Name is required')])
    last_name = StringField('Last Name', validators=[DataRequired(message='Last Name is required')])
    email = StringField('Email', validators=[DataRequired(message='Email is required'), Email()])
    password = PasswordField('Password', validators=[DataRequired(message='Password is required'), Length(min=6)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(message='Confirm password is required'), EqualTo('password')])
    submit = SubmitField('Register')

class SettingsForm(FlaskForm):
    name = StringField('First Name', validators=[DataRequired(message='First Name is required')])
    last_name = StringField('Last Name', validators=[DataRequired(message='Last Name is required')])
    email = StringField('Email', validators=[DataRequired(message='Email is required'), Email()])
    old_password = PasswordField('Old Password', validators=[DataRequired(message='Password is required'), Length(min=6)])
    new_password = PasswordField('New Password', validators=[])
    confirm_password = PasswordField('Confirm New Password', validators=[EqualTo('new_password', message='Passwords must match')])
    submit = SubmitField('Save')

   
class ProductAddForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(message='Name is required')])
    description = TextAreaField('Description', validators=[DataRequired(message='Description is required')])
    file_data = FileField('Upload ZIP File', validators=[DataRequired(message='ZIP File is required')])
    id_user = StringField('User ID', validators=[DataRequired(message='User ID is required')])
    submit = SubmitField('Add')


class ProductEditForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(message='Name is required')])
    description = TextAreaField('Description', validators=[DataRequired(message='Description is required')])
    file_zip_path = StringField('File Zip Path')
    id_user = StringField('User ID', validators=[DataRequired(message='User ID is required')])

    file_data = FileField('Upload new ZIP File?')
    submit = SubmitField('Save')
