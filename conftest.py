import pytest
import os

from helpers.helpers import get_fixtures

pytest_plugins = get_fixtures()

print(os.environ["DATABASE_URL"])
