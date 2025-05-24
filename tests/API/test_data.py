from uuid import uuid4
import sys

class TestData:
# if category_id = 1 : подставится категории для класса тестов
    test_create_product = [
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
        ),
        (
            {"name": ('0'*19)+f"{str(uuid4())}",
            "description": "длина name более 50",
            "price": 999.99,
            "category_id": 1}, 400
        ),
        (
            {"name": f"длина description более 50{str(uuid4())}",
            "description": ('0'*19)+f"{str(uuid4())}",
            "price": 999.99,
            "category_id": 1}, 400
        )
    ]
