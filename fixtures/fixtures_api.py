from helpers.helpers import get_settings
import pytest
from requests import Session
from api.category_api import CategoryApi
from api.product_api import ProductApi
from uuid import uuid4


settings_config = get_settings()
api_session = None


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart():
    global api_session
    api_session = Session()


@pytest.fixture(scope='function')
def get_settings_and_session_api():
    return {'session': api_session, 'settings': settings_config}


@pytest.fixture(scope='function')
def category_api():
    return CategoryApi(api_base_url=settings_config['API_URL'], session=api_session)


@pytest.fixture(scope='function')
def product_api():
    return ProductApi(api_base_url=settings_config['API_URL'], Session=api_session)

@pytest.fixture(scope='function')
def get_random_category(category_api):
    category = category_api.create_new_category(data={'name':f'test_category_{str(uuid4())}'})
    assert category.status_code == 200
    return category.json()
