from api.base_api import BaseApi

class CategoryApi(BaseApi):
    def create_new_category(self, data):
        return self.send_post(url='/categories/', data=data)
    
    def read_categories(self):
        return self.send_get(url='/categories/')
    
    def read_category(self, category_id):
        return self.send_get(url=f"/categories/{category_id}")