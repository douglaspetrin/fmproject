from fmapi.models import db


def add_instance(model, **kwargs):
    instance = model(**kwargs)
    db.session.add(instance)
    commit_changes()


def commit_changes():
    db.session.commit()
