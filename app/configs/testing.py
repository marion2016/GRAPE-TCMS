import os

from .default import ROOT_PATH
from .default import *  # NOQA F401


TEST_BASE_DIR = os.path.join(ROOT_PATH, '.test')
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(
    os.path.join(TEST_BASE_DIR, 'GRAPE-TCMS.db'))
# SQLALCHEMY_ECHO = True
TESTING = True

if not os.path.exists(TEST_BASE_DIR):
    os.makedirs(TEST_BASE_DIR)
