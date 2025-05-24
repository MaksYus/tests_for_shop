import pytest
from uuid import uuid4

from models.models import Product
from helpers.db import DB
from tests.API.test_data import TestData


class TestProducts:
    # status_code проставляется дальше по ходу теста.
    @pytest.mark.parametrize("product_data, status_code", TestData.test_create_product)
    def test_create_product(self, product_data, status_code,  product_api, get_random_category_class, get_settings_and_session_postgre):
        # Создаем товар
        if product_data["category_id"] == 1:
            product_data["category_id"] = get_random_category_class['id']
        response = product_api.create_new_product(data=product_data)

        assert response.status_code == status_code
        if status_code != 200:
            return 1
        assert response.json() == product_data

        db = DB(session=get_settings_and_session_postgre['session'])
        db_data = db.get(table_name=Product,
                         condition=response.json(), limit=1)
        assert db_data
        assert len(db_data) == 1

        assert db.delete(table_name=Product, condition=response.json())

    def test_read_product(self, product_api, get_random_category_class, get_settings_and_session_postgre):
        response_for_create = product_api.create_new_product(data={"name": f"Тестовый продукт_{str(uuid4())}",
                                                                   "description": "Описание продукта",
                                                                   "price": 999.99,
                                                                   "category_id": get_random_category_class["id"]
                                                                   }
                                                             )
        assert response_for_create.status_code == 200
        created_product = response_for_create.json()
        response = product_api.read_product(product_id=created_product["id"])
        assert response.status_code == 200
        assert response.json() == created_product

        db = DB(session=get_settings_and_session_postgre['session'])
        assert db.delete(table_name=Product, condition=created_product)

    def test_read_products(self, product_api, get_random_category_class, get_settings_and_session_postgre):
        created_products = []
        count_prods = 5
        for _ in range(count_prods):
            response_for_create = product_api.create_new_product(data={"name": f"Тестовый продукт_{str(uuid4())}",
                                                                       "description": "Описание продукта",
                                                                       "price": 999.99,
                                                                       "category_id": get_random_category_class["id"]
                                                                       }
                                                                 )
            assert response_for_create.status_code == 200
            created_products.append(response_for_create.json())

        response = product_api.read_products()
        assert response.status_code == 200
        products = response.json()
        assert len(products) == count_prods

        for product in products:
            assert product in created_products

        db = DB(session=get_settings_and_session_postgre['session'])
        for created_product in created_products:
            assert db.delete(table_name=Product, condition=created_product)

    def test_read_category_products(self, product_api, category_api, get_settings_and_session_postgre):
        # создаём 2 категории
        create_response = category_api.create_new_category(
            data={"name": f"Категория 1 _ {str(uuid4())}"})
        assert create_response.status_code == 200
        category_1 = create_response.json()
        assert category_1
        create_response = category_api.create_new_category(
            data={"name": f"Категория 2 _ {str(uuid4())}"})
        assert create_response.status_code == 200
        category_2 = create_response.json()
        assert category_2

        # получаю список продуктов в категории
        created_products = []
        count_prods = 5
        for _ in range(count_prods):
            response_for_create = product_api.create_new_product(data={"name": f"Тестовый продукт_{str(uuid4())}",
                                                                       "description": "Описание продукта",
                                                                       "price": 999.99,
                                                                       "category_id": category_1["id"]
                                                                       }
                                                                 )
            assert response_for_create.status_code == 200
            created_products.append(response_for_create.json())

        response = product_api.read_product_from_category(category_1["id"])
        assert response.status_code == 200
        products_from_response = response.json()

        # получаю данные из БД остальных источников
        db = DB(session=get_settings_and_session_postgre['session'])
        products_from_db = db.get(table_name=Product, condition={
                                  "category_id": category_1["id"]})
        assert len(products_from_db) == count_prods

        # проверки
        for product in products_from_response:
            assert product["category_id"] == category_1["id"]
            assert product in products_from_db
            assert product in created_products
