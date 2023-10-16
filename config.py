from dotenv import dotenv_values

env_config = dotenv_values(".env")


class Config(object):
    SECRET_KEY = env_config["SECRET_KEY"]
    DB = env_config["DB"]
    SQLALCHEMY_DATABASE_URI = env_config.get("DB")
    CACHE_TYPE = env_config.get("CACHE_TYPE")
    CACHE_REDIS_HOST = env_config.get("CACHE_REDIS_HOST")
    CACHE_REDIS_PORT = env_config.get("CACHE_REDIS_PORT")
    CACHE_REDIS_DB = env_config.get("CACHE_REDIS_DB")
    CACHE_REDIS_URL = env_config.get("CACHE_REDIS_URL")
    CACHE_DEFAULT_TIMEOUT = env_config.get("CACHE_DEFAULT_TIMEOUT")


class ProductionConfig(Config):
    DEBUG = False
    DEVELOPMENT = False

class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True

class TestingConfig(Config):
    DB = env_config["TESTING_DB"]
    SQLALCHEMY_DATABASE_URI = env_config.get("TESTING_DB")