from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import json
import hmac
import base64
import hashlib

app = FastAPI()

# Base de données fictive
users_db = {"admin": "admin"}
orders = []

# Clé secrète et algorithme pour le JWT
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

# Gestion des tokens OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authenticate")


def base64url_encode(data):
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")

def base64url_decode(data):
    padding = '=' * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)

def create_access_token(data):
    header = {"alg": ALGORITHM, "typ": "JWT"}
    header_encoded = base64url_encode(json.dumps(header).encode())
    payload_encoded = base64url_encode(json.dumps(data).encode())
    signature = hmac.new(SECRET_KEY.encode(), f"{header_encoded}.{payload_encoded}".encode(), hashlib.sha256).digest()
    signature_encoded = base64url_encode(signature)
    return f"{header_encoded}.{payload_encoded}.{signature_encoded}"

def verify_access_token(token):
    try:
        header_encoded, payload_encoded, signature_encoded = token.split(".")
        signature_check = hmac.new(SECRET_KEY.encode(), f"{header_encoded}.{payload_encoded}".encode(), hashlib.sha256).digest()
        expected_signature = base64url_encode(signature_check)
        if hmac.compare_digest(signature_encoded, expected_signature):
            return json.loads(base64url_decode(payload_encoded))
    except Exception:
        pass
    return None

class LoginRequest(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    password: str

class OrderCreate(BaseModel):
    product: str
    quantity: int

class OrderUpdate(BaseModel):
    product: str | None = None
    quantity: int | None = None

@app.post("/authenticate")
def login(request: LoginRequest):
    if request.username in users_db and users_db[request.username] == request.password:
        token = create_access_token({"sub": request.username})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/users")
def create_user(user: UserCreate):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    users_db[user.username] = user.password
    return {"message": "User created"}

@app.get("/orders")
def get_orders(token: str = Security(oauth2_scheme)):
    user = verify_access_token(token)
    if user:
        return {"orders": orders, "user": user["sub"]}
    raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/orders")
def create_order(order: OrderCreate, token: str = Security(oauth2_scheme)):
    user = verify_access_token(token)
    if user:
        new_order = {"id": len(orders) + 1, "product": order.product, "quantity": order.quantity, "user": user["sub"]}
        orders.append(new_order)
        return new_order
    raise HTTPException(status_code=401, detail="Invalid token")

@app.put("/orders/{order_id}")
def update_order(order_id: int, order: OrderCreate, token: str = Security(oauth2_scheme)):
    user = verify_access_token(token)
    if user:
        for existing_order in orders:
            if existing_order["id"] == order_id and existing_order["user"] == user["sub"]:
                existing_order["product"] = order.product
                existing_order["quantity"] = order.quantity
                return existing_order
        raise HTTPException(status_code=404, detail="Order not found or not authorized")
    raise HTTPException(status_code=401, detail="Invalid token")

@app.patch("/orders/{order_id}")
def partial_update_order(order_id: int, order: OrderUpdate, token: str = Security(oauth2_scheme)):
    user = verify_access_token(token)
    if user:
        for existing_order in orders:
            if existing_order["id"] == order_id and existing_order["user"] == user["sub"]:
                if order.product is not None:
                    existing_order["product"] = order.product
                if order.quantity is not None:
                    existing_order["quantity"] = order.quantity
                return existing_order
        raise HTTPException(status_code=404, detail="Order not found or not authorized")
    raise HTTPException(status_code=401, detail="Invalid token")

@app.delete("/orders/{order_id}")
def delete_order(order_id: int, token: str = Security(oauth2_scheme)):
    user = verify_access_token(token)
    if user:
        for i, existing_order in enumerate(orders):
            if existing_order["id"] == order_id and existing_order["user"] == user["sub"]:
                del orders[i]
                return {"message": "Order deleted"}
        raise HTTPException(status_code=404, detail="Order not found or not authorized")
    raise HTTPException(status_code=401, detail="Invalid token")
