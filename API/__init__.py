import config

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from flask_migrate import Migrate
from utils.redis_manager import RedisManager

from utils.uuid_url_converter import UUIDConverter

db = SQLAlchemy()
base = declarative_base()


def create_app(conf=config.ProductionConfig):
    app = Flask(__name__)
    app.url_map.converters["uuid"] = UUIDConverter
    app_settings = conf
    app.config.from_object(app_settings)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSON_AS_ASCII"] = False
    app.config["JSON_SORT_KEYS"] = False

    db.init_app(app)
    Migrate(app, db)
    app.e = create_engine(app.config["DB"], pool_size=5, pool_recycle=5)

    # Register Blueprints

    from API.ticket.views import ticket_api

    app.register_blueprint(ticket_api)

    app.redis = RedisManager().get_client()
    return app
