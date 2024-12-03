from functools import wraps

from fastapi import FastAPI, Header, Depends, HTTPException
from pydantic import validator

from redis_module import Redis
from pydantic import BaseModel
import redis

app = FastAPI()


class Params(BaseModel):
    key: str
    value: str
    token:str

    @validator("token")
    def check_token(cls, token):
        if len(token) < 5:
            raise ValueError("Len of token must be greater than 5")
        return token



def redis_client():
    return redis.StrictRedis(host="localhost", port="6379", db=0)

def valid_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = kwargs.get("params")
        print(token.token)
        if token.token != "12345":
            raise HTTPException(status_code=401, detail="Unauthorized")
        return func(*args, **kwargs)
    return wrapper


def cached(func):
    @wraps(func)
    def wrapper(key, client, *args, **kwargs):
        if not client.exists(key):
            raise HTTPException(status_code=404, detail="Record with this name doesn't found")
        #return func(key, *args, **kwargs)
        return {f"{key}": f"{client.get(f'{key}').decode('utf-8')}"}
    return wrapper



@app.get("/get_record")
@cached
def get_record(key:str, client = Depends(redis_client)):
    pass


@app.post("/create_record")
#@valid_token
def post_record(params: Params, client = Depends(redis_client)):
    client.set(params.key, params.value)
    return {"message": f"{client.get(params.key).decode('utf-8')}"}


