from base64 import b64encode

import pytest

from blogapp.views import create_app
from blogapp.database import db
from blogapp.models import Article, Category, Tag

@pytest.fixture
def app():
    app = create_app(test=True)
    return app

@pytest.fixture(scope="module")
def test_db():
    db.create_all()
    yield db
    db.drop_all(app=app())

@pytest.fixture()
def truncate():
    yield None
    db.session.query(Tag).delete()
    db.session.query(Article).delete()
    db.session.query(Category).delete()
    db.session.commit()

headers_authorization = {
    'Authorization': b'Basic ' + b64encode(b'test:')
}
