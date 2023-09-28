from pydantic import BaseModel

class GuestMessage(BaseModel):
    message: str

class AdminMessage(BaseModel):
    message: str

class MenuItem(BaseModel):
    name: str
    type: str
    price: float

class Order(BaseModel):
    id: int
    total: float

class Upsell(BaseModel):
    id_oders: int

class OrderItem(BaseModel):
    id_orders: int
    id_menu: int
    name: str
    price: float
