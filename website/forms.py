from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email


class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired("Please provide your first name.")])
    last_name = StringField('Last Name', validators=[DataRequired("Please provide your last name.")])
    organization = StringField("Affiliated Organization",
                               validators=[DataRequired("Please provide your affiliated Organization.")])
    email = EmailField('Email Address', validators=[DataRequired("Please provide an email address."),
                                            Email('Please provide a valid email address.')])
    submit = SubmitField('Register')

class NNForm(FlaskForm):
    #Todo The validator for ID must be pulled from a sql database.
    id = StringField('ID Code', validators=[DataRequired("Please enter ID code provided to you via email")])
    pdb_struct = StringField('PDB Structure', validators=[DataRequired("Please provide a PDB structure.")])
    submit = SubmitField('Submit')

