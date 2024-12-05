from functools import wraps
from fastapi import FastAPI, Depends, HTTPException
from pydantic import validator
from starlette.middleware.base import BaseHTTPMiddleware
from create import create_task, create_user
from connect import Session
from models import Tasks, Users
from pydantic import BaseModel
from create import get_task
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


products = {'0': 100, '1': 200}

class Value(BaseModel):
    id: str
    qty: int

class User(BaseModel):
    name:str
    password:str

class Userr(BaseModel):
    name: str
    role: str
    send_limit: int


class Resource(BaseModel):
    id: int
    role_require: str

user = {'Kate': {'role': 'admin', 'send_limit': 5}, 'Alice': {'role': 'user', 'send_limit': 3}}


def check_permission(user: Userr, resource: Resource):
    if user.role == resource.role_require:
        return True
    return False




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
        flag = True
        if not client.exists(key):
            flag = False
            with Session() as session:
                client.set(key, get_task(key, session))
            #raise HTTPException(status_code=404, detail="Record with this name doesn't found in cache, now it's cached")
            return {f"{key}": f"{client.get(f'{key}').decode('utf-8')}", "cached": f"{flag}"}
        #return func(key, *args, **kwargs)
        return {f"{key}": f"{client.get(f'{key}').decode('utf-8')}", "cached": f"{flag}"}
    return wrapper

#Пример мидлвары из доки
# @app.middleware("http")
# def middleware_func(request: Request, call_next):
#     print("middleware working")
#     response = call_next(request)
#     return response


class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        print(f"Request received: {request.url}")
        response = await call_next(request)

        # Модификация ответа, если нужно
        response.headers['X-Custom-Header'] = 'Value'

        return response

    # Добавление middleware в приложение
app.add_middleware(CustomMiddleware)



@app.get("/get_record")
@cached
async def get_record(key:str, client = Depends(redis_client)):
    pass


@app.post("/create_record")
#@valid_token
async def post_record(params: Params, client = Depends(redis_client)):
    #client.set(params.key,params.value, ex=3600)
    #return params
    task = Tasks(name=params.key, value=params.value)
    with Session() as session:
        message = create_task(task, session)
        return message
    # return {"message": f"{client.get(params.key).decode('utf-8')}"}


@app.post("/params")
async def params(value: Value):
    total = 0
    total += products[value.id]*value.qty
    return total


@app.post("/reg")
async def reg(user:User):
    with Session() as session:
        o = Users(user.name, user.password)
        return create_user(o, session)


@app.post('/{resource_id}')
async def resource(id:int, user: Userr):
    resources = Resource(id=id, role_require='admin')
    if check_permission(user, resources):
        return {"message": "success"}
    return {"message": "forbidden"}