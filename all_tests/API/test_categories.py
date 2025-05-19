import pytest
from contextlib import nullcontext as does_not_raise


@pytest.mark.all
@pytest.mark.categories
class TestCategories:

    @pytest.mark.todo
    @pytest.mark.parametrize("name, expectation",
                      [
                            ("Электроника", does_not_raise()),
                            ("с пробелом", does_not_raise()),
                            ("""спец.символы /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]+/""", does_not_raise()),
                            (None, does_not_raise()),
                            (5, does_not_raise()),
                            ("", does_not_raise()),
                            ("Электроника", does_not_raise())
                       ])
    def test_create_category(self, name, expectation, client):
        with expectation:
            response = client.post(
                "/categories/",
                json={"name": name}
            )
            assert response.status_code == 200
            assert response.json()["name"] == name

    def test_read_category(self, client):
        create_response = client.post(
            "/api/v1/categories/",
            json={"name": "Одежда"}
        )
        category_id = create_response.json()["id"]

        response = client.get(f"/categories/{category_id}")
        assert response.status_code == 200
        assert response.json()["name"] == "Одежда"

        response = client.get(f"/categories/-1")
        assert response.status_code == 404

    def test_update_category(self, client):
        # Создаем
        create_response = client.post(
            "/api/v1/categories/",
            json={"name": "Книги"}
        )
        category_id = create_response.json()["id"]

        # Обновляем
        update_response = client.put(
            f"/api/v1/categories/{category_id}",
            json={"name": "Книги и журналы"}
        )
        assert update_response.status_code == 200
        assert update_response.json()["name"] == "Книги и журналы"

    def test_delete_category(self, client):
        # Создаем
        create_response = client.post(
            "/categories/",
            json={"name": "Мебель"}
        )
        category_id = create_response.json()["id"]

        # Удаляем
        delete_response = client.delete(f"/api/v1/categories/{category_id}")
        assert delete_response.status_code == 204

        # Проверяем что удалилось
        get_response = client.get(f"/api/v1/categories/{category_id}")
        assert get_response.status_code == 404
