from blogapp.views import create_app
import pytest

@pytest.fixture
def app():
    app = create_app(test=True)
    return app
