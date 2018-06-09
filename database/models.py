from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Quote
class Quote(db.Model):
    __tablename__ = "quotes"
    id    = db.Column(db.Integer, primary_key=True)
    words = db.Column(db.String(240), unique=True)
    category = db.Column(db.String(120))

    def __init__(self, words, category):
        self.words = words
        self.category = category

    def __repr__(self):
        return '<Quote %r>' % self.words

