from fastapi import FastAPI, Path
from datetime import datetime
import calendar
import os
import requests
from google.cloud import firestore
                    
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "firebase_key.json"

app = FastAPI()

db = firestore.Client()


@app.get("/hello")
def read_root():
    return {"data": "Hello World"}

@app.get("/add")
def add_to_firestore():
    now = datetime.now()
    day_of_week = calendar.day_name[now.weekday()]
    day_of_month = now.day
    month = now.strftime('%b') 

    data = {
        "day_of_week": day_of_week,
        "day_of_month": day_of_month,
        "month": month,
        "timestamp": firestore.SERVER_TIMESTAMP,
    }

    doc_ref = db.collection("NewsTok_test_collection").add(data)
    return {"status": "Success", "document_id": doc_ref[1].id}


FAKESTORE_API = "https://fakestoreapi.com"

@app.get("/products")
def get_all_products():
    response = requests.get(f"{FAKESTORE_API}/products")
    return response.json()


@app.post("/cart/add/{product_id}")
def add_to_cart(product_id: int = Path(..., description="Product ID to add")):
    payload = {
        "userId": 1,
        "date": str(datetime.now().date()),
        "products": [{"productId": product_id, "quantity": 1}]
    }
    response = requests.post(f"{FAKESTORE_API}/carts", json=payload)
    return response.json()

@app.get("/cart")
def list_cart():
    response = requests.get(f"{FAKESTORE_API}/carts")
    return response.json()

@app.put("/cart/update/{cart_id}")
def update_cart(cart_id: int):
    payload = {
        "userId": 1,
        "date": str(datetime.now().date()),
        "products": [{"productId": 2, "quantity": 5}]
    }
    response = requests.put(f"{FAKESTORE_API}/carts/{cart_id}", json=payload)
    return response.json()

@app.delete("/cart/delete/{cart_id}")
def delete_cart(cart_id: int):
    response = requests.delete(f"{FAKESTORE_API}/carts/{cart_id}")
    return response.json()
