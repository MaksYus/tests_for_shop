def test_create_order(client):
    # Создаем категорию и товар
    category_response = client.post(
        "/api/v1/categories/",
        json={"name": "Электроника"}
    )
    category_id = category_response.json()["id"]

    product_response = client.post(
        "/api/v1/products/",
        json={
            "name": "Наушники",
            "price": 199.99,
            "category_id": category_id
        }
    )
    product_id = product_response.json()["id"]

    # Создаем заказ
    order_data = {
        "customer_name": "Иван Иванов",
        "customer_email": "ivan@example.com",
        "items": [{"product_id": product_id, "quantity": 2}]
    }
    response = client.post("/api/v1/orders/", json=order_data)

    assert response.status_code == 201
    assert response.json()["customer_name"] == "Иван Иванов"
    assert len(response.json()["items"]) == 1
    assert response.json()["total_amount"] == 399.98  # 199.99 * 2
