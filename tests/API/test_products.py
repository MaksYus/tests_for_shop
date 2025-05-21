import pytest
from uuid import uuid4
import sys
import random

from models.models import Product
from helpers.db import DB


class TestProducts:
    @pytest.mark.todo
    def test_create_product(self, product_api, get_settings_and_session_postgre):
        # Сначала создаем 
        response = product_api.create_new_product(data={"name": f"Тестовый продукт_{str(uuid4())}",
                                                        "description": "Описание продукта",
                                                        "price": 123.123,
                                                        "category_id": 1
                                                        })
        assert response.status_code == 200

        category_id = category_response.json()["id"]

        # Создаем товар
        product_data = {
            "name": "Смартфон",
            "description": "Флагман 2023",
            "price": 999.99,
            "category_id": category_id
        }
        response = client.post("/api/v1/products/", json=product_data)

        assert response.status_code == 201
        assert response.json()["name"] == "Смартфон"
        assert response.json()["category_id"] == category_id

    def test_get_products_by_category(client):
        # Создаем категорию и товары
        category_response = client.post(
            "/api/v1/categories/",
            json={"name": "Одежда"}
        )
        category_id = category_response.json()["id"]

        client.post("/api/v1/products/", json={
            "name": "Футболка",
            "price": 19.99,
            "category_id": category_id
        })

        # Получаем товары по категории
        response = client.get(f"/api/v1/categories/{category_id}/products")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["name"] == "Футболка"
