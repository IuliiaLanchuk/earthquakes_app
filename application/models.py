
from application import db

import requests

class Saver:
    def save(self):
        db.session.add(self)
        db.session.commit()


class User(db.Model, Saver):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), unique = True)
    city = db.Column(db.String(51), db.ForeignKey('location.city'))
    age = db.Column(db.Integer)

    def __repr__(self):
        return '<User %r> from <%r>' % (self.nickname, self.city)


class Location(db.Model, Saver):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), db.ForeignKey('user.city'), unique=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    citizens = db.relationship('User', backref='citizen')

    def __repr__(self):
        return '<Location %r - latitude %r and longitude %r>' % (self.city, self.latitude, self.longitude)
