from config import *
from sqlalchemy_utils import database_exists,create_database

subscription_table =db.Table('subscription_table',
                db.Column('user_id', db.Integer, db.ForeignKey('people.user_id'), primary_key=True),
                db.Column('article_id', db.Integer, db.ForeignKey('article.article_id'), primary_key=True)
                )

class People(db.Model):
    __tablename__ = 'people'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), nullable=False)
    user_email=db.Column(db.String(100),unique=True,nullable=False)
    subsriptions = db.relationship('Article', secondary=subscription_table, backref='subscibers')

    def __init__(self, name,email):
        self.user_name = name
        self.user_email=email

class Article(db.Model):
    __tablename__ = 'article'
    article_id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(10), nullable=False)
    content = db.Column(db.String(100), nullable=False)

    def __init__(self,topic,content):
        self.topic=topic
        self.content=content

def add_article():
    for loop in range(10):
        db.session.add(Article(topic='topic'+str(loop+1),content='content'+str(loop+1)))
        db.session.commit()

if not database_exists(SQLAlCHEMY_DATABASE_URI):
    create_database(SQLAlCHEMY_DATABASE_URI)
db.create_all()
db.session.commit()
add_article()


#add_article()