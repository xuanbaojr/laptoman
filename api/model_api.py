from fastapi import FastAPI
from fastapi.responses import Response

from typing import Union
from pydantic import BaseModel

class Item(BaseModel):
    input:str

app = FastAPI()

@app.post("/click/")
def click(test: Item):
    return test.input
