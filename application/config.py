import os


class Config:

    # Set up the App SECRET_KEY
    SECRET_KEY = os.environ['SECRET_KEY']

    # This will create a file in <app> FOLDER
    basedir = os.path.abspath(os.path.dirname(__file__))

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db_instance.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
