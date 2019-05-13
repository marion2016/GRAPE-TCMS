import os

ROOT_PATH = os.path.split(os.path.abspath(__name__))[0]

DEBUG = True
SECRET_KEY = 'TPuvPsiWSgrAQXIyxfzWbvPAyzrILVGSPxpSCH'
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(
    os.path.join(ROOT_PATH, 'GRAPE-TCMS.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False

CELERY_TIMEZONE = 'Asia/Shanghai'
BROKER_URL = 'sqla+sqlite:///celerydb.sqlite'  # CELERY_BROKER_URL
CELERY_RESULT_BACKEND = 'db+sqlite:///results.sqlite'
