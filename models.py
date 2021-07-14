import os
from sqlalchemy import Column, String, Integer, DateTime, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
from dotenv import load_dotenv

#----------------------------------------------------------------------------#
# Connect the database and environment variables
#----------------------------------------------------------------------------#

load_dotenv()

if os.getenv('ENV') == 'test':
    database_path = os.getenv('TEST_DATABASE_URL')
else:
    # SQLAlchemy 1.4 removed support for postgres://
    # Heroku sets the DATABASE_URL to this and can't be changed
    # https://help.heroku.com/ZKNTJQSK/why-is-sqlalchemy-1-4-x-not-connecting-to-heroku-postgres
    database_path = os.environ['DATABASE_URL']
    if database_path.startswith('postgres://'):
        database_path = database_path.replace('postgres://', 'postgresql://', 1)

db = SQLAlchemy()

'''
setup_db(app)
    Binds a flask app to a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # print(f'Connecting to: {database_path}')
    # migrate = Migrate(app, db)

'''
db_drop_and_create()
    Drops the database and creates an an empty one
'''
def db_drop_and_create():
    db.drop_all()
    db.create_all()

#----------------------------------------------------------------------------#
# Movie table
#----------------------------------------------------------------------------#
class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(DateTime(), nullable=False)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date
    
    '''
    insert()
        Inserts a new movie into the database
        The title and release date must not be null
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    update()
        Updates fields of an existing movie
        The title and relase date must not be null
    '''
    def update(self):
        db.session.commit()

    '''
    delete()
        Deletes a movie from the database matching the sent id
        If the movie does not exist a 404 error is sent
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    format()
        returns the movie as an object
    '''
    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

    def __repr__(self):
        return f'id: {self.id} title: {self.title} release date: {self.release_date}'