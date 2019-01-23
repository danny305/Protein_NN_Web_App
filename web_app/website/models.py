from itsdangerous import URLSafeTimedSerializer
from sqlalchemy.schema import CheckConstraint
from datetime import datetime, timedelta
import jwt

from flask import url_for, render_template, make_response, redirect

from . import app,db, bcrypt
from tools import send_email



class Users(db.Model):
    __tablename__ = "Users"
    #ToDo create a column for the unique token of a user.
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(length=255), nullable=False)
    last_name = db.Column(db.String(length=255), nullable=False)
    email = db.Column(db.String(length=80), index=True, unique=True, nullable=False)
    password = db.Column(db.String(length=255),nullable=False)
    organization = db.Column(db.String(length=255),nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    confirmation_link_sent_on = db.Column(db.DateTime, nullable=True)
    email_confirmed = db.Column(db.Boolean, nullable=True, default=False)
    email_confirmed_on = db.Column(db.DateTime, nullable=True)
    queries = db.relationship("NN_Query",backref="user", lazy='dynamic')


    def __init__(self,first,last,email,password,organization, confirmation_link_sent_on=None):
        self.first_name = first
        self.last_name = last
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode()
        self.registered_on = datetime.now()
        self.organization = organization
        self.confirmation_link_sent_on = confirmation_link_sent_on
        self.email_confirmed = False
        self.email_confirmed_on = None

    def __repr__(self):
        return '<User %s %s <%s> from %s>' % \
               (self.first_name, self.last_name, self.email, self.organization)


    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=0,minutes=30,seconds=0),
                'iat': datetime.utcnow(),
                'sub': user_id
            }

            return jwt.encode(payload=payload,
                              key=app.config.get('JWT_SECRET_KEY'),
                              algorithm='HS256'
                              )

        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token,key=app.config.get('JWT_SECRET_KEY'))
            return payload['sub']

        except jwt.ExpiredSignatureError:
            return "Signature Expired. Please login again."

        except jwt.InvalidTokenError:
            return "Invalid Token. Please login again."


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        app.logger.info('Successfully saved to DB.')


    def check_pw(self,form_pw):
        return bcrypt.check_password_hash(self.password,form_pw)


    def check_user_confirmed(self):
        app.logger.info('check if user confirmed: {}'.format(self.email_confirmed))
        return self.email_confirmed


    def confirm_email(self):
        self.email_confirmed = True
        self.save_to_db()
        app.logger.info('Email confirmed and updated DB: {}'.format(self.email_confirmed))
        return self.email_confirmed


    def send_confirmation_email(self):
        if not self.email_confirmed:
            confirm_serializer = URLSafeTimedSerializer(app.config['MAIL_SECRET_KEY'])
            token = confirm_serializer.dumps(self.email, salt=app.config['MAIL_SALT'])
            confirmation_url = url_for('confirm_email_endpoint', token=token, _external=True)
            html = render_template('email_confirmation_2.html', confirm_url=confirmation_url)
            try:
                send_email("Confirm Email",
                           [self.email, app.config['MAIL_DEFAULT_SENDER']],
                           html_body=html)
                app.logger.info('successfully sent email from : {}'.format(app.config['MAIL_DEFAULT_SENDER']))
            except Exception as e:
                print('Error occurred while sending {} their confirmation email.\n'.format(self.email), e)
                app.logger.error('Error occurred while sending {} their confirmation email.\n'.format(self.email), e)
                return False

            return True

        else:
            print("{} had their email confirmed on {}".format(self.email, self.email_confirmed_on))


class NN_Query(db.Model):

    __tablename__ = "NN_Query"

    id= db.Column(db.Integer,primary_key=True)
    #ToDo I need to assign the time stamp in the init not as class variable.
    pdb_query = db.Column(db.String(length=8),nullable=True)
    protein_file = db.Column(db.String(), nullable=True)
    query_time = db.Column(db.DateTime, index=True, nullable=False)
    user_email = db.Column(db.Integer, db.ForeignKey('Users.email'))

    __table_args__ = CheckConstraint('NOT(pdb_query IS NULL AND protein_file IS NULL)'),


    def __init__(self,query,user_email):
        if len(query) < 8:
            self.pdb_query = query
        else:
            self.protein_file = query

        self.user_email = user_email
        self.query_time = datetime.now()


    def __repr__(self):
        return "<NN_Query {}>".format(self.pdb_query)

