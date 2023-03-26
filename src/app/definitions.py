# app/definitions.py
from enum import Enum
from pydantic import BaseModel
from os import getenv

# The file simulates a fake database for the data
DATABASE = getenv('FAKEAPI_DATABASE', 'data.json')
# The interface Uvicorn listens
HOSTNAME = getenv('FAKEAPI_INTF', '0.0.0.0')
# The TCO port for Uvicorn
PORT = int(getenv('FAKEAPI_PORT', 8000))

tags_metadata = [
    {
        "name": "root",
        "description": "Example of the **GET** method REST API on the root.",
    },
    {
        "name": "get",
        "description": "Example of the **GET** method REST API.",
    },
    {
        "name": "post",
        "description": "Example of the **POST** method REST API.",
    },
    {
        "name": "put",
        "description": "Example of the **PUT** method REST API.",
    },
    {
        "name": "patch",
        "description": "Example of the **PATCH** method REST API.",
    },
    {
        "name": "head",
        "description": "Example of the **HEAD** method REST API.",
    },
    {
        "name": "trace",
        "description": "Example of the **TRACE** method REST API.",
    },
    {
        "name": "options",
        "description": "Example of the **OPTIONS** method REST API.",
    },
    {
        "name": "delete",
        "description": "Example of the **DELETE** method REST API.",
    },
    # {
    #     "name": "items",
    #     "description": "Manage items. So _fancy_ they have their own docs.",
    #     "externalDocs": {
    #         "description": "Items external docs",
    #         "url": "https://fastapi.tiangolo.com/",
    #     },
    # },
]

class Category(Enum):
    CLOTHES = 'clothes'
    GROCERY = 'grocery'
    TOOLS = 'tools'
    CONSUMABLES = 'consumables'

class Item(BaseModel):
    id: int
    description: str
    price: float
    quantity: int
    category: Category

# The URLs for the 'patchItem' function
class PatchURL(str, Enum):
    price = "price"
    quantity = "quantity"
    description = "description"

class ItemID(BaseModel):
    item_id: int

class IDPrice(BaseModel):
    item_id: int
    price: float

class IDQuantity(BaseModel):
    item_id: int
    quantity: int


items = [
    Item(id=100, description="Hammer", price=9.99, quantity=20, category=Category.TOOLS),
    Item(id=101, description="Jeans", price=39.99, quantity=100, category=Category.CLOTHES),
    Item(id=102, description="Apple", price=0.50, quantity=150, category=Category.GROCERY),
    Item(id=103, description="Radio AM/FM", price=25.49, quantity=5, category=Category.CONSUMABLES),
]
