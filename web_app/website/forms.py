from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, EqualTo, length, Regexp, Optional

from models import Users
from tools import NoneRegExp, OrTo, send_confirmation_email

from . import app

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[
                                           DataRequired("Please provide your first name."),
                                                     length(min=2,max=128),
                                                      ])

    last_name = StringField('Last Name', validators=[
                                         DataRequired("Please provide your last name."),
                                                     length(min=2, max=128),
                                                    ])

    organization = StringField("Affiliated Organization",
                               validators=[DataRequired("Please provide your affiliated Organization."),
                                           length(min=6, max=128),
                                            #ToDo write validator to check for multiple words to make sure its nots an acryonym
                                           ])

    email = EmailField('Email Address', validators=[
                                        DataRequired("Please provide an email address."),
                                                    Email('Please provide a valid email address.'),
                                                    length(min=8, max=128),
                                                    Regexp('.+@.+\.edu$', message="Currently only academic email "
                                                                                  "addresses are accepted. (.edu)"),
                                                    ])

    retype_email = EmailField('Confirm Email Address', validators=[
                                                    DataRequired("Please retype your email address."),
                                                    Email('Please provide a valid email address.'),
                                                    length(min=8, max=128),
                                                    EqualTo('email',message='Emails did not match.'),
                                                    ])

    password = PasswordField("Password", validators=[
                                         DataRequired("Please provide a password"),
                                         length(min=8, max=128),
                                         # NoneRegExp('^([^0-9]*|[^A-Z]*|[^a-z]*|[^0-9A-Za-z ]*)$',
                                         #            message='Password must contain at least 1 capital, lowercase, '
                                         #                    'number, and symbol.\nPassword must be at least 8 '
                                         #                    'characters long.'),
                                         ])

    retype_password = PasswordField("Confirm Password", validators=[
                                                        DataRequired("Please retype your password"),
                                                        length(min=8, max=128),
                                                        EqualTo('password',message='Passwords did not match.'),
                                                        ])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = EmailField("Email Address", validators=[
                                        DataRequired("Please provide your email address."),
                                        Email('Make sure you typed in your email correctly.'),
                                        length(min=8, max=128),
                                        ])

    password = PasswordField("Password", validators=[
                                        DataRequired("Please provide your password"),
                                        length(min=8, max=128),
                                        NoneRegExp('^([^0-9]*|[^A-Z]*|[^a-z]*|[^0-9A-Za-z ]*)$',
                                            message='Password must contain at least 1 capital, lowercase, number, '
                                                    'and symbol.\nPassword must be at least 8 characters long.'),
                                        ])
    submit = SubmitField('Login')

    # def __init__(self):
    #     super(LoginForm,self).__init__()

    def validate(self):
        user = Users.query.filter_by(email=self.email.data).first()
        if user:
            if user.check_pw(self.password.data):
                if user.email_confirmed == True:
                    #I must return the user object bc this is a callback assigned to a variable.
                    print('User email has been confirmed')
                    app.logger.info('Email address for: {} has been confirmed.'.format(user.email))
                    return user
                else:
                    self.email.errors = ('Email address has not been confirmed. New link sent.',) #This must be a tuple
                    user.send_confirmation_email()
                    app.logger.error('User: {} has not confirmed email address. New confirmation linked '
                                     'sent'.format(user.email))
                    return False
            else:
                self.password.errors = ('Incorrect password.',)
                app.logger.error('User: {} has entered an incorrect email'.format(user.email))
                return False
        else:
            self.email.errors = ('Unknown email address.',) #This must be a tuple
            app.logger.error('Unknown email address has attempted to login.')
            return False


class NNForm(FlaskForm):
    #Todo The validator for email must be pulled from a sql database/JWT from the user.

    #ToDo need to figure out the validators to use for the protein submission.
    pdb_struct = StringField('PDB Structure', validators=[
                                        Optional("Please provide a PDB structure."),
                                        ])

    cryst_struct_file = FileField("Crystal Structure File", validators=[
                                                            OrTo('pdb_struct'),
                                                                ])

    submit = SubmitField('Submit')

    def validate(self):
        if self.pdb_struct.data and self.cryst_struct_file.data:
            self.cryst_struct_file.errors ="Form only accepts a PDB structure or a " \
                                          "crystal structure file but not both.",
            return False
        elif self.pdb_struct.data:
                if len(self.pdb_struct.data) == 4:
                    self.query = self.pdb_struct.data.upper()
                    return True
                else:
                    self.pdb_struct.errors = 'Invalid PDB ID: longer or shorter than 4 characters.',
                    return False
        elif self.cryst_struct_file.data:
            self.query = self.cryst_struct_file
            return True
        else:
            return False

