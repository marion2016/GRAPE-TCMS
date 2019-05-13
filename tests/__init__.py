from flask_sqlalchemy import model

from app.run import app, db


class BaseTest:
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    @classmethod
    def setup_class(cls):
        with app.app_context():
            db.create_all()

    @classmethod
    def teardown_class(cls):
        with app.app_context():
            db.drop_all()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        for m in [m for m in db.Model._decl_class_registry.values()
                  if isinstance(m, model.DefaultMeta)]:
            db.session.query(m).delete()
        db.session.commit()
