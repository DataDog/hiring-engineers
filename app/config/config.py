import os
from app import ENVIRONMENT

if ENVIRONMENT == 'dev':
    SQLALCHEMY_DATABASE_URI="postgresql://datadog@localhost/datadog_db"
else:
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URI')

SQLALCHEMY_TRACK_MODIFICATIONS=True
