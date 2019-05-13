import pytest

from app.run import app as tapp


@pytest.fixture(scope='session')
def app(request):
    ctx = tapp.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return tapp


@pytest.fixture(scope='session')
def client(app, request):
    return app.test_client()


@pytest.fixture(scope='session')
def celery_config(app):
    return {
        'broker_url': 'sqla+sqlite:///.test/celerydb.sqlite',
        'result_backend': 'db+sqlite:///.test/celeryresults.sqlite'
    }


@pytest.fixture(scope='session')
def celery_app(app):
    from app.run import celery
    from celery.contrib.testing import tasks  # NOQA
    return celery
