from website import db

from datetime import datetime


class RegUsers(db.Model):
    __tablename__ = "Users"
    #ToDo create a column for the unique token of a user.
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(length=20), nullable=False)
    last_name = db.Column(db.String(length=20), nullable=False)
    email = db.Column(db.String(length=80), index=True, unique=True, nullable=False)
    organization = db.Column(db.String(length=50),nullable=False)
    queries = db.relationship("NN_Query",backref="user", lazy='dynamic')


    def __init__(self,first,last,email,organization):
        self.first_name = first
        self.last_name = last
        self.email = email
        self.organization = organization

    def __repr__(self):
        return '<User %s %s %r>' % self.first_name, self.last_name, self.email




class NN_Query(db.Model):

    id= db.Column(db.Integer,primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    query = db.Column(db.String(length=8),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))


    def __repr__(self):
        return "<NN_Query {}".format(self.query)

