from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import create_app
from models import db, Movie, Actor

app = create_app()

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def seed():
    Movie(title='Call Me By Your Name', release_date='1/19/2018').insert()
    Movie(title='The Boys in the Band', release_date='9/30/2020').insert()

    Actor(name='Timothee Chalamet', age=26, gender='male').insert()
    Actor(name='Zachary Quinto', age=44, gender='male').insert()

if __name__ == '__main__':
    manager.run()