""" Documentation
ทำหน้าที่เชื่อมต่อ Database และทำหน้าที่จัดการ Applications Interface (API)

Example:
    ตัวอย่างการเรียกใช้ไฟล์ fast.py
        $ uvicorn fast:app --reload
"""
from typing import Union
from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World", "Fast": "Checking"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
