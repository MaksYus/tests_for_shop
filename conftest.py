import pytest
from sqlalchemy import create_engine
from fixtures import fixtures_api, fixtures_db

import os

engine = create_engine(os.getenv("DATABASE_URL"))
print(os.getenv("DATABASE_URL"))
