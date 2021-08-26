from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length

# Login Form class for admin
class LoginForm(FlaskForm):
    username = StringField('Username',validators = [InputRequired(),Length(min = 4,max = 15)])
    password = PasswordField('Password',validators = [InputRequired(),Length(min = 4,max = 80)])
    rememberme = BooleanField('Remember Me')