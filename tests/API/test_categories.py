import pytest
from contextlib import nullcontext as does_not_raise
from uuid import uuid4
import sys
import random

from models.models import Category
from helpers.db import DB


class TestCategories:

    @pytest.mark.parametrize("name, status_code",
                             [
                                 (f"с пробелом {str(uuid4())}", 200),
                                 (f"""спец.символы /[!@#$%^&*()_+\-=\[\];':"\\|,.<>\/?]+/{str(uuid4())}""", 200),
                                 (None, 422),
                                 (random.randint(0, sys.maxsize-1), 200),
                                 ("", 400),
                                 ("Электроника", 400),
                                 ("0"*(19)+f"{str(uuid4())}", 200) # в сумме длина 19 + 32 = 51
                             ])
    def test_create_category(self, name, status_code, category_api, get_settings_and_session_postgre):

        response = category_api.create_new_category(data={"name": name})

        # проверка http ответа
        assert response.status_code == status_code
        if response.status_code != 200:
            return 1
        assert response.json()["name"] == name

        db = DB(session=get_settings_and_session_postgre['session'])
        # проверка наличия записи в базе
        db_data = db.get(table_name=Category,
                         condition=response.json(), limit=1)
        assert db_data
        assert len(db_data) == 1

        # удаляю добавленные данные
        assert db.delete(table_name=Category, condition={'name': name})

    def test_read_category(self, category_api, get_settings_and_session_postgre):
        # создаю данные для получения
        category_name = f"Одежда_{str(uuid4())}"
        create_response = category_api.create_new_category(
            data={"name": category_name})
        category_id = create_response.json()["id"]

        # получаю созданные данные
        response = category_api.read_category(category_id)
        assert response.status_code == 200
        assert response.json()["name"] == category_name

        db = DB(session=get_settings_and_session_postgre['session'])
        db_data = db.get(table_name=Category, condition=response.json())
        assert db_data
        assert len(db_data) == 1
        assert db_data[0] == response.json()

        # удаляю добавленные данные
        assert db.delete(table_name=Category, condition={'name': category_name})

        response = category_api.read_category(-1)
        assert response.status_code == 404
        assert response.json()['detail'] == "Category not found"

    def test_read_all_categories(self, category_api, get_settings_and_session_postgre):
        # создаём категории
        random_uuid = str(uuid4())
        create_response_1 = category_api.create_new_category(
            data={"name": f"Одежда_{random_uuid}"})
        create_response_2 = category_api.create_new_category(
            data={"name": f"Электроника_{random_uuid}"})

        response = category_api.read_categories()
        assert response.status_code == 200
        assert len(response.json()) >= 2

        db = DB(session=get_settings_and_session_postgre['session'])
        all_categories = db.get(table_name=Category, condition={})

        assert create_response_1.json() in response.json()
        assert create_response_2.json() in response.json()

        assert create_response_1.json() in all_categories
        assert create_response_2.json() in all_categories
