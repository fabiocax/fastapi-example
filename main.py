from fastapi import FastAPI 
from oauth import main as auth
from example import main as example

app = FastAPI()
app.include_router(auth.oauth)
app.include_router(example.example)

@app.get("/")
async def root():
    return {"message": "Diretorio Root"}
