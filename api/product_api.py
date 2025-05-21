from api.base_api import BaseApi

class ProductApi(BaseApi):
    def create_new_product(self, data):
        return self.send_post(url='/products/', data=data)
    
    def read_products(self):
        return self.send_get(url='/products/')
    
    def read_product(self, product_id):
        return self.send_get(url=f"/products/{product_id}")