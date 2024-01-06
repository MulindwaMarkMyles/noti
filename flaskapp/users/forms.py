from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length,  EqualTo, ValidationError
from flaskapp.models import User
from validate_email_address import validate_email 
from flask_login import current_user

class RegistrationForm(FlaskForm):
        username = StringField("Username", validators=[DataRequired(), Length(min=2, max=30)])
        email = StringField("Email", validators=[DataRequired()])
        password = PasswordField("Password", validators=[DataRequired()])
        confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
        submit = SubmitField('Sign Up')
        
        def validate_username(self, username):
                user = User.query.filter_by(username=username.data).first()
                if user:
                        raise ValidationError("The username is already taken!")
        
        def validate_email(self, email):
                if email.data.__contains__(' '):
                        email.data = email.data.strip()
                if validate_email(email.data):
                        user = User.query.filter_by(email=email.data).first()
                        if user:
                                raise ValidationError("That email is already taken!")
                else:
                        raise ValidationError("That email is invalid!")
                        

class LoginForm(FlaskForm):
        email = StringField("Email", validators=[DataRequired()])
        password = PasswordField("Password", validators=[DataRequired()])
        remember = BooleanField('Remember Me')
        submit = SubmitField('Login')
        
        def validate_email(self, email):
                if email.data.__contains__(' '):
                        email.data = email.data.strip()
                if not validate_email(email.data):
                        raise ValidationError("That email is invalid!")
        
class UpdateAccountForm(FlaskForm):
        username = StringField("Username:", validators=[DataRequired(), Length(min=2, max=30)])
        email = StringField("Email:", validators=[DataRequired()])
        picture = FileField("Change Profile Picture", validators=[FileAllowed(["jpeg","jpg","png"])])
        submit = SubmitField('Update')
                
        def validate_username(self, username):
                if username.data != current_user.username:
                        user = User.query.filter_by(username=username.data).first()
                        if user:
                                raise ValidationError("The username is already taken!")
        
        def validate_email(self, email):
                if email.data.__contains__(' '):
                        email.data = email.data.strip()
                if validate_email(email.data) and email.data != current_user.email:
                        user = User.query.filter_by(email=email.data).first()
                        if user:
                                raise ValidationError("That email is already taken!")
                else:
                        raise ValidationError("That email is invalid!")
                        
class RequestResetForm(FlaskForm):
        email = StringField("Email", validators=[DataRequired()])
        submit = SubmitField("Request Password Reset")
        
        def validate_email(self, email):
                if email.data.__contains__(' '):
                        email.data = email.data.strip()
                if validate_email(email.data):
                        user = User.query.filter_by(email=email.data).first()
                        if not user:
                                raise ValidationError("That email appears not to be in our database!")
                else:
                        raise ValidationError("That email is invalid!")
                
class ResetPasswordForm(FlaskForm):
        password = PasswordField("Password", validators=[DataRequired()])
        confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
        submit = SubmitField("Reset Password")