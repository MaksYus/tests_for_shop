from helpers.helpers import get_settings
import pytest
from requests import Session
from uuid import uuid4

from models.models import Category
from api.category_api import CategoryApi
from api.product_api import ProductApi
from helpers.db import DB


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
def get_random_category(category_api, get_settings_and_session_postgre):
    category = category_api.create_new_category(data={'name':f'test_category_{str(uuid4())}'})
    assert category.status_code == 200
    yield category.json()

    # удаление созданной категории
    db = DB(session=get_settings_and_session_postgre['session'])
    assert db.delete(table_name=Category, condition={'name': category.json()})

@pytest.fixture(scope='class')
def get_random_category_class(get_random_category):
    yield get_random_category