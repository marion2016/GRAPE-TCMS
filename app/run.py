import logging

from flask import Flask, request
from flask.helpers import get_env

from hobbit_core.flask_hobbit.err_handler import ErrHandler

from app.exts import db, migrate, ma, hobbit, celery
from app import views


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    hobbit.init_app(app)


def register_blueprints(app):
    app.register_blueprint(views.ping.bp, url_prefix='/api')


def register_error_handler(app):
    app.register_error_handler(Exception, ErrHandler.handler)


def register_cmds(app):
    pass


def make_celery(app):
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    from app import tasks  # NOQA
    return celery


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('app.configs.{}'.format(get_env()))

    register_extensions(app)
    register_blueprints(app)
    register_error_handler(app)
    register_cmds(app)
    make_celery(app)

    @app.before_request
    def log_request_info():
        logger = logging.getLogger('werkzeug')
        if request.method in ['POST', 'PUT']:
            logger.info('Body: %s', request.get_data())

    return app


app = create_app()
