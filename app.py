from dataclasses import dataclass, field
from typing import ClassVar
import uuid
from fastapi import FastAPI
class ProductValidationError(Exception): pass
class ProductNotFoundError(Exception): pass


@dataclass
class Product:
    name: str
    p_type: str
    id : int = field(default_factory=lambda: str(uuid.uuid4()), init=False)

    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ProductValidationError("Product name must not be empty !!")

class ProductManager: 
    def __init__(self):
        self._products = {}

    def add_prouduct(self, product: Product) -> None:
        self._products[product.id] = product
        print(f" Prouduct {product.name} with Id : {product.id} has been added")
    def find_products(self, name: str) -> Product:
        if name not in self._products:
            ProductNotFoundError()
    def delete_product(self, productId: str) -> Product: 
        if productId not in self._products:
            ProductNotFoundError()
        del self._products[productId]
    def list_all(self) -> list[Product]:
        return list(self._products.values())

           
app = FastAPI(title="Product management micro service")
repo = ProductManager()

repo.add_prouduct(Product("rice", "rice"))
repo.add_prouduct(Product("Dal", "Pulses"))

@app.get('/')
def default():
    return "OK"

@app.get("/get_all")
def getall():
    return repo.list_all()

@app.post("/product")
def add_product(name: str, type: str):
    repo.add_prouduct(Product(name, type))