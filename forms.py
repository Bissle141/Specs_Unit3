from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators, IntegerField

class LoginForm(FlaskForm):
   username = StringField('Username', [validators.InputRequired()])
   password = PasswordField('Password', [validators.InputRequired()])
   
class AddQuanMelonCartForm(FlaskForm):
   quantity = IntegerField('Quantity', [validators.NumberRange(min=1, max=10)], default=1)
