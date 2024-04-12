import uvicorn
from fastapi import FastAPI

from tortoise.contrib.fastapi import register_tortoise
from settings.settings import TORTOISE_ORM

from api.user import *

app = FastAPI()

app.include_router(user_api)

register_tortoise(
    app=app,
    config=TORTOISE_ORM
)

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8888, reload=True, workers=1)
