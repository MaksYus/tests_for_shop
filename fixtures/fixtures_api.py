from helpers.helpers import get_settings
import pytest
from requests import Session

settings_config = get_settings()
api_session = None

@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart():
    global api_session
    api_session = Session()