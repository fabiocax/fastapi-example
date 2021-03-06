
from fastapi import APIRouter, Form,Depends

from models import Base , engine, SessionLocal, Users
from sqlalchemy.orm import sessionmaker
from os import environ
from dependencies import *
import requests

example = APIRouter(
    prefix="/example/v1",
    tags=["example"],
    dependencies=[Depends(get_current_active_user)],
    responses={404: {"description": "Not found"}},
)


@example.post("/teste/" )
async def compare_texts(text1: str = Form(...),text2: str = Form(...), current_user: User = Depends(get_current_active_user)):
    ret=text1+" "+text2+" On user:"+str(current_user)
    return ret


@example.post("/address/{cep}")
async def search_address_by_cep(cep: str):
    response = requests.get(f"http://viacep.com.br/ws/{cep}/json/")
    return response.json()