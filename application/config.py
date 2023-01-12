import os


class Config:

    # Set up the App SECRET_KEY
    SECRET_KEY = os.environ['SECRET_KEY']

    # This will create a file in <app> FOLDER
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
