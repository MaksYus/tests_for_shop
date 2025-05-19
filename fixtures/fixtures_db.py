from sqlalchemy.ext.declarative import declarative_base

import pytest
import os

from helpers.db import DB
from helpers.helpers import get_settings
from uuid import uuid4
from models.models import Category

settings_config = {}
postgre_session = DB()

@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart():
    global settings_config, postgre_session
    settings_config = get_settings()
    if os.getenv('POSTGRES_USER') != '' and os.getenv('POSTGRES_PASSWORD') != '':
        postgre_session = DB().create_session()


@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish():
    if os.getenv('POSTGRES_USER') != '' and os.getenv('POSTGRES_PASSWORD') != '':
        postgre_session.close()

@pytest.fixture(scope='function')
def insert_remove_category():
    random_name_category = f"generated_category_{str(uuid4())}"
    model = Category(
        session=postgre_session,
        data={
            'name': random_name_category
        }
    )
    model.insert(query=model)
    yield model

    model.remove(condition={'id':model.id})