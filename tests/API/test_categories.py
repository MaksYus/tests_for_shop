import pytest
from contextlib import nullcontext as does_not_raise
from uuid import uuid4
import sys
import random

from models.models import Category


@pytest.mark.all
@pytest.mark.categories
class TestCategories:

    @pytest.mark.todo
    @pytest.mark.parametrize("name, status_code",
                             [
                                 (f"Электроника_{str(uuid4())}", 200),
                                 (f"с пробелом {str(uuid4())}", 200),
                                 (f"""спец.символы /[!@#$%^&*()_+\-=\[\];':"\\|,.<>\/?]+/{str(uuid4())}""",200),
                                 (None, 422),
                                 (random.randint(0,sys.maxsize), 200),
                                 ("",400),
                                 ("Электроника", 500)
                             ])
    def test_create_category(self, name, status_code, category_api, get_settings_and_session_postgre):

        response = category_api.create_new_category(data={"name": name})

        # проверка http ответа
        assert response.status_code == status_code
        assert response.json()["name"] == name

        # проверка наличия записи в базе
        db_cat = Category(
            session=get_settings_and_session_postgre['session'])
        assert db_cat.get(table_name=Category,
                            condition=response.json()).len() > 0

        # удаляю добавленные данные
        db_cat.delete(table_name=Category, condition={'name': name})

    def test_read_category(self, category_api, get_settings_and_session_postgre):
        create_response = category_api.create_new_category(
            data={"name": "Одежда"})
        category_id = create_response.json()["id"]

        response = category_api.read_category(category_id)
        assert response.status_code == 200
        assert response.json()["name"] == "Одежда"

        db_cat = Category(session=get_settings_and_session_postgre['session'])
        assert db_cat.get(table_name=Category, condition=response.json())[
            0] == create_response.json()

        response = category_api.read_category("-1")
        assert response.status_code == 404
        assert response.description == "Category not found"

    def test_read_all_categories(self, category_api, get_settings_and_session_postgre):
        create_response_1 = category_api.create_new_category(
            data={"name": "Одежда"})
        create_response_2 = category_api.create_new_category(
            data={"name": "Электроника"})

        response = category_api.read_categories()
        assert response.status_code == 200
        assert response.json().len() >= 2

        db_cat = Category(session=get_settings_and_session_postgre['session'])
        all_categories = db_cat.get(table_name=Category)

        assert create_response_1.json() in response.json()
        assert create_response_2.json() in response.json()

        assert create_response_1.json() in all_categories
        assert create_response_2.json() in all_categories
