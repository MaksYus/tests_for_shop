from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from helpers.db import BASE, DB


class Category(DB, BASE):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    products = relationship("Product", back_populates="category")

    def __init__(self, session, data=None):
        super().__init__(session)
        self.name = data["name"]

    def get_first_record(self):
        return self.get(table_name=Category, limit=1)

    def insert(self, query):
        return self.create(query_object=query)

    def remove(self, condition):
        return self.delete(table_name=Category, condition=condition)


class Product(DB, BASE):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")


class Order(DB, BASE):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String)
    customer_email = Column(String)
    shipping_address = Column(String)
    total_amount = Column(Float)

    items = relationship("OrderItem", back_populates="order")


class OrderItem(DB, BASE):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    price = Column(Float)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
