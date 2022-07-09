from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def root():
    return {"Hello": "World"}


@app.get('/user')
async def get_user():
    return {"User": "user"}


@app.get('/login')
async def login():
    return {"User": "Status-Success"}
