from fastapi import APIRouter, Depends, HTTPException
from dependencies import *
from fastapi import FastAPI,status,HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from models import  engine, Users
from sqlalchemy.orm import sessionmaker
import random
import hashlib
from dependencies import *

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v2/token")

def uuid():
	return hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()

Session = sessionmaker(bind=engine)
session = Session()

oauth = APIRouter(
    prefix="/api",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

@oauth.post("/v2/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
	userdb=session.query(Users).filter(Users.username == form_data.username,Users.disabled==False).one()
	users_db={form_data.username:userdb.as_dict()}
	user = authenticate_user(users_db, form_data.username, form_data.password)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Incorrect username or password",
			headers={"WWW-Authenticate": "Bearer"},
		)
	access_token_expires = timedelta(minutes=userdb.token_timeout)
	access_token = create_access_token(
		data={"sub": user.username}, expires_delta=access_token_expires
	)
	return {"access_token": access_token, "token_type": "bearer"}

@oauth.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
	return current_user
