import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

app = Flask(__name__)
app.config.from_object('application.config.Config')

db = SQLAlchemy(app, metadata=MetaData(naming_convention={
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}))
db.init_app(app)


def init_app():
    with app.app_context():
        # Create sql tables for our data models
        from application.routes import page

        db.create_all()
        app.register_blueprint(page)

    return app


Migrate(app, db)


from application import models
from application import routes

if __name__=='__main__':
    # -*- coding: utf-8 -*-
    port = int(os.environ.get('PORT', 5000))
    init_app().run(host='0.0.0.0', port=port, debug=True)

