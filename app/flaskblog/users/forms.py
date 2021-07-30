from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(max=20, min=2)])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = StringField('password', validators=[DataRequired()])
    confirm_password = StringField('confirm_password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign_up')

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = StringField('password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    login = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(max=20, min=2)])
    email = StringField('email', validators=[DataRequired(), Email()])
    picture = FileField('Update profile_pic', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

class RequestToken(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request password reset')

class ResetPasswordForm(FlaskForm):
    password = StringField('password', validators=[DataRequired()])
    confirm_password = StringField('confirm_password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Reset Password')