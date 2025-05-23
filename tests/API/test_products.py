import pytest
from uuid import uuid4
import sys

from models.models import Product
from helpers.db import DB


class TestProducts:
    # status_code проставляется дальше по ходу теста.
    @pytest.mark.parametrize("product_data, status_code",
                             [
                                 (
                                     {"name": f"Тестовый продукт_{str(uuid4())}",
                                      "description": "Описание продукта",
                                      "price": 999.99,
                                      "category_id": 1}, 200
                                 ),
                                 (
                                     {"name": f"Тестовый продукт_{str(uuid4())}",
                                      "description": "отрицательная длина",
                                      "price": -1,
                                      "category_id": 1}, 400
                                 ),
                                 (
                                     {"name": f"""спец.символы /[!@#$%^&*()_+\-=\[\];':"\\|,.<>\/?]+/{str(uuid4())}""",
                                      "description": f"""спец.символы /[!@#$%^&*()_+\-=\[\];':"\\|,.<>\/?]+/{str(uuid4())}""",
                                      "price": 123,
                                      "category_id": 1}, 200
                                 ),
                                 (
                                     {"name": f"Тестовый продукт_{str(uuid4())}",
                                      "description": f"Тестовый продукт_{str(uuid4())}",
                                      "price":  sys.maxsize-1,
                                      "category_id": 1}, 200
                                 ),
                                 (
                                     {"name": f"Тестовый продукт_{str(uuid4())}",
                                      "description": "не существующий category_id",
                                      "price": 999.99,
                                      "category_id": -1}, 400
                                 )
                             ]
                             )
    @pytest.mark.todo
    def test_create_product(self, product_api, get_random_category_class, get_settings_and_session_postgre):
        # Создаем товар
        product_data = {
            "name": f"Тестовый продукт_{str(uuid4())}",
            "description": "Описание продукта",
            "price": 999.99,
            "category_id": get_random_category_class['id']
        }
        response = product_api.create_new_product(data=product_data)

        assert response.status_code == 200
        assert response.json() == product_data

        db = DB(session=get_settings_and_session_postgre['session'])
        db_data = db.get(table_name=Product,
                         condition=response.json(), limit=1)
        assert db_data
        assert len(db_data) == 1
