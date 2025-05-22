import pytest
from uuid import uuid4
import sys
import random

from models.models import Product
from helpers.db import DB


class TestProducts:
    @pytest.mark.todo
    def test_create_product(self, product_api, get_random_category, get_settings_and_session_postgre):
        # Создаем товар
        product_data = {
            "name": f"Тестовый продукт_{str(uuid4())}",
            "description": "Описание продукта",
            "price": 999.99,
            "category_id": get_random_category['id']
        }
        response = product_api.create_new_product(data=product_data)

        assert response.status_code == 200
        assert response.json() == product_data

        db = DB(session=get_settings_and_session_postgre['session'])
        db_data = db.get(table_name=Product,
                         condition=response.json(), limit=1)
        assert db_data
        assert len(db_data) == 1