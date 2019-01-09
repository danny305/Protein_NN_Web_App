from website import app,db, bcrypt

from sqlalchemy.schema import CheckConstraint
from datetime import datetime, timedelta
import jwt
#from flask_jwt_extended import


class Users(db.Model):
    __tablename__ = "Users"
    #ToDo create a column for the unique token of a user.
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(length=20), nullable=False)
    last_name = db.Column(db.String(length=20), nullable=False)
    email = db.Column(db.String(length=80), index=True, unique=True, nullable=False)
    password = db.Column(db.String(length=25),nullable=False)
    organization = db.Column(db.String(length=50),nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    queries = db.relationship("NN_Query",backref="user", lazy='dynamic')


    def __init__(self,first,last,email,password,organization):
        self.first_name = first
        self.last_name = last
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode()
        self.registered_on = datetime.now()
        self.organization = organization


    def __repr__(self):
        return '<User %s %s <%s> from %s>' % (self.first_name, self.last_name, self.email, self.organization)


    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=0,seconds=5),
                'iat': datetime.utcnow(),
                'sub': user_id
            }

            return jwt.encode(payload=payload,
                              key=app.config.get('SECRET_KEY'),
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
            payload = jwt.decode(auth_token,key=app.config.get('SECRET_KEY'))
            return payload['sub']

        except jwt.ExpiredSignatureError:
            return "Signature Expired. Please login again."

        except jwt.InvalidTokenError:
            return "Invalid Token. Please login again."


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    def check_pw(self,form_pw):
        return bcrypt.check_password_hash(self.password,form_pw)


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

