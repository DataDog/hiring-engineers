from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Quotes
class Quote(db.Model):
    __tablename__ = "quotes"
    id    = db.Column(db.Integer, primary_key=True)
    words = db.Column(db.String(360), unique=True)
    category = db.Column(db.String(120))

    def __init__(self, words, category):
        self.words = words
        self.category = category

    def __repr__(self):
        return '<Quote %r>' % self.words

# Users
class User(db.Model):
    __tablename__ = "users"
    id    = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    team     = db.Column(db.String(40))

    def __init__(self, username, team):
        self.username = username
        self.team = team

    def __repr__(self):
        return '<Username %r>' % self.username
