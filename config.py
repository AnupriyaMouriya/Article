from app import app
from flask_sqlalchemy import SQLAlchemy

POSTGRES_URL = "10.110.42.29:5432"
POSTGRES_USER = "postgres"
POSTGRES_PW = "hellopizza"
POSTGRES_DB = "database"

SQLAlCHEMY_DATABASE_URI='postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER, pw=POSTGRES_PW,
                                                                                     url=POSTGRES_URL, db=POSTGRES_DB)

app.config['SQLALCHEMY_DATABASE_URI']=SQLAlCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)