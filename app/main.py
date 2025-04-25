
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
import time, uuid

app = FastAPI(title="Store API", version="0.1.0")
_bearer = HTTPBearer(auto_error=False)

tokens: dict[str, str] = {}   # token -> username
carts:  dict[str, list] = {}  # username -> [items]

PRODUCTS = [
    {"id": 1, "name": "Sauce Labs Backpack",       "price": 29.99},
    {"id": 2, "name": "Sauce Labs Bike Light",     "price": 9.99},
    {"id": 3, "name": "Sauce Labs Bolt T-Shirt",   "price": 15.99},
    {"id": 4, "name": "Sauce Labs Fleece Jacket",  "price": 49.99},
    {"id": 5, "name": "Sauce Labs Onesie",         "price": 7.99},
    {"id": 6, "name": "Test.allTheThings() Shirt", "price": 15.99},
]

# quick lookup so we don't loop every time
_product_map = {p["id"]: p for p in PRODUCTS}


# models

class LoginReq(BaseModel):
    username: str
    password: str

class CartItem(BaseModel):
    product_id: int
    qty: int = 1

class CheckoutReq(BaseModel):
    first_name: str
    last_name: str
    zip_code: str


#auth dependency

def get_current_user(creds: Optional[HTTPAuthorizationCredentials] = Depends(_bearer)) -> str:
    if not creds or creds.credentials not in tokens:
        raise HTTPException(401, "not authenticated")
    return tokens[creds.credentials]

#routes
@app.get("/health")
def health():
    return {"status": "ok", "ts": time.time()}


@app.post("/auth/login")
def login(body: LoginReq):
    if body.password != "secret_sauce":
        raise HTTPException(401, "bad credentials")
    tok = uuid.uuid4().hex
    tokens[tok] = body.username
    carts[body.username] = []
    return {"token": tok, "username": body.username}


@app.post("/auth/logout")
def logout(user: str = Depends(get_current_user)):
    carts.pop(user, None)
    return {"message": "logged out"}


@app.get("/products")
def list_products():
    return PRODUCTS


@app.get("/products/{pid}")
def get_product(pid: int):
    p = _product_map.get(pid)
    if not p:
        raise HTTPException(404, "product not found")
    return p


@app.post("/cart")
def add_to_cart(item: CartItem, user: str = Depends(get_current_user)):
    if item.product_id not in _product_map:
        raise HTTPException(404, "product not found")
    carts.setdefault(user, []).append({
        "product_id": item.product_id,
        "qty": item.qty,
    })
    return {"cart": carts[user]}


@app.get("/cart")
def view_cart(user: str = Depends(get_current_user)):
    return {"cart": carts.get(user, [])}


@app.post("/checkout")
def checkout(body: CheckoutReq, user: str = Depends(get_current_user)):
    cart = carts.get(user, [])
    if len(cart) == 0:
        raise HTTPException(400, "cart is empty")

    total = 0.0
    for item in cart:
        prod = _product_map.get(item["product_id"])
        if prod:
            total += prod["price"] * item["qty"]

    oid = f"ORD-{uuid.uuid4().hex[:8].upper()}"
    num_items = len(cart)
    carts[user] = []  # clear after checkout

    return {
        "order_id": oid,
        "total": round(total, 2),
        "items": num_items,
        "shipping": f"{body.first_name} {body.last_name}, {body.zip_code}",
    }
