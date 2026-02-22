import pytest

def test_app_import():
    from app import create_app
    app = create_app()
    assert app is not None


def test_app_responds():
    from app import create_app
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as c:
        rv = c.get('/')
    assert rv.status_code in [200, 302]
