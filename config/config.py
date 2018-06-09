import os

#SQLALCHEMY_DATABASE_URI="postgresql://datadog@localhost/datadog_db"
SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS=True
