import requests


class ProductClient:

    @staticmethod
    def get_products():
        r = requests.get("http://product-api:5002/api/products", timeout=5)
        return r.json()

    @staticmethod
    def get_product(slug):
        r = requests.get(f"http://product-api:5002/api/product/{slug}", timeout=5)
        return r.json()
