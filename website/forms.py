from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, EqualTo, length

from website.models import Users


class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[
                                           DataRequired("Please provide your first name."),
                                                     length(min=3,max=20),
                                                      ])

    last_name = StringField('Last Name', validators=[
                                         DataRequired("Please provide your last name."),
                                                     length(min=3, max=20),
                                                    ])

    organization = StringField("Affiliated Organization",
                               validators=[DataRequired("Please provide your affiliated Organization."),
                                           length(min=6, max=50),
                                           ])

    email = EmailField('Email Address', validators=[
                                        DataRequired("Please provide an email address."),
                                                    Email('Please provide a valid email address.'),
                                                    length(min=8, max=50),
                                                    ])

    retype_email = EmailField('Confirm Email Address', validators=[
                                                    DataRequired("Please retype your email address."),
                                                    Email('Please provide a valid email address.'),
                                                    length(min=8, max=50),
                                                    EqualTo('email'),
                                                    ])

    password = PasswordField("Password", validators=[
                                         DataRequired("Please provide a password"),
                                         length(min=8, max=25),
                                         ])

    retype_password = PasswordField("Confirm Password", validators=[
                                                        DataRequired("Please retype your password"),
                                                        length(min=8, max=25),
                                                        EqualTo('password'),
                                                        ])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = EmailField("Email Address", validators=[
                                        DataRequired("Please provide your email address."),
                                        Email('Make sure you typed in your email correctly.'),
                                        length(min=8, max=50),
                                        ])

    password = PasswordField("Password", validators=[
                                        DataRequired("Please provide your password"),
                                        length(min=8, max=25),
                                        ])
    submit = SubmitField('Login')

    # def __init__(self):
    #     super(LoginForm,self).__init__()

    def validate(self):
        user = Users.query.filter_by(email=self.email.data).first()
        if user:
            if user.check_pw(self.password.data):
                return user
            else:

                self.password.errors = ('Incorrect password.',)
                return False
        else:
            self.email.errors = ('Unknown email address.',)
            return False

    
class NNForm(FlaskForm):
    #Todo The validator for email must be pulled from a sql database/JWT from the user.
    email = EmailField("Email Address", validators=[
                                        DataRequired("Please provide your email address."),
                                        Email('Make sure you typed in your email correctly.'),
                                        length(min=8, max=50),
                                        ])

    #ToDo need to figure out the validators to use for the protein submission.
    pdb_struct = StringField('PDB Structure', validators=[
                                        DataRequired("Please provide a PDB structure."),
                                        ])

    cryst_struct_file = FileField("Crystal Structure File", validators=[
                                                            "None",
                                                                ])

    submit = SubmitField('Submit')


    def __init__(self,form,headers):
        self.headers=headers
        super(NNForm,self).__init__(form)

    def validate(self):
        user = self.headers
        print(user)
        #print([item for item in user['Cookie'].split(';') if item.startswith('session')])
        #ToDo this is where the logic goes to pull the PDB structure from pdb.org
        #ToDo This is where the logic goes to submit a crystal structure file to the NN.
        pass
