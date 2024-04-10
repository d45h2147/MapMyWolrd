"""Flask configuration."""
from sqlalchemy.pool import NullPool
from os import path, urandom, getenv
from logging.handlers import RotatingFileHandler
import logging
import os


DB_USER = getenv('DB_USER')
DB_PASSWORD = getenv('DB_PASSWORD')
DB_NAME = getenv('DB_NAME')
DB_DRIVE = getenv('DB_DRIVE')
DB_HOST = getenv('DB_HOST')
ALLOWED_ORIGINS = getenv('ALLOWED_ORIGINS')
ENV_SERVER_PATH = path.abspath(path.join(path.dirname(__file__), ''))
ENV_SECRET_KEY = urandom(34).hex()
LOG_FORMAT = '%(asctime)s %(levelname)s: [%(filename)s:%(lineno)d - %(funcName)s()] %(message)s'


class Config(object):
    """
    Common configurations
    """
    SERVER_PATH = ENV_SERVER_PATH
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    SQLALCHEMY_ENGINE_OPTIONS = {"poolclass": NullPool}
    # SQLALCHEMY_DATABASE_URI = f'{DB_DRIVE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{ENV_SERVER_PATH}/db/mapmyworld.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_BINDS = {}
    
    if ALLOWED_ORIGINS:
        ALLOWED_ORIGINS = ALLOWED_ORIGINS.split(',')
    else:
        ALLOWED_ORIGINS = []

    PROPAGATE_EXCEPTIONS = True
    BUNDLE_ERRORS = True

    @staticmethod
    def init_app(app, log_level, log_file):
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler(
            log_file, maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        file_handler.setLevel(log_level)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(log_level)


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    FLASK_DEBUG = True
    # SENTRY_ENV = "dev"
    @staticmethod
    def init_app(app):
        super(DevelopmentConfig, DevelopmentConfig).init_app(
            app, logging.DEBUG, 'logs/development.log'
        )


class QualityConfig(Config):
    """
    QA Ambient configurations
    """
    FLASK_DEBUG = False
    # SENTRY_ENV = "qty"

    @staticmethod
    def init_app(app):
        super(QualityConfig, QualityConfig).init_app(
            app, logging.INFO, 'logs/quality.log'
        )


class ProductionConfig(Config):
    """
    Production configurations
    """
    FLASK_DEBUG = False
    # SENTRY_ENV = "pro"
    SWAGGER_URL="http://localhost/swagger"
    @staticmethod
    def init_app(app):
        super(ProductionConfig, ProductionConfig).init_app(
            app, logging.WARNING, 'logs/production.log'
        )


app_config = {
    'dev': DevelopmentConfig,
    'qty': QualityConfig,
    'pro': ProductionConfig
}
