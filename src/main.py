from functools import wraps
from jinja2 import Environment, FileSystemLoader
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Request
from pydantic import validator
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from create import create_task, create_user, get_task_id
from connect import Session
from models import Tasks, Users
from pydantic import BaseModel
from create import get_task
import redis
from fastapi.openapi.utils import get_openapi

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
    login:str
    token:str

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
            try:
                with Session() as session:
                    client.set(key, get_task(key, session))
                    data = get_task(key, session)
                #raise HTTPException(status_code=404, detail="Record with this name doesn't found in cache, now it's cached")
                return {f"{key}": f"{client.get(f'{key}').decode('utf-8')}", "cached": f"{flag}"}
            except:
                return {f"No record with this key"}
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
async def get_record(request:Request, key:str, client = Depends(redis_client)):
    cached_data = client.get(key)
    if cached_data:
        data = cached_data.decode('utf-8')
        templates = Jinja2Templates(directory='C:\\Users\\AdminIS\\micreservice\\templates')
        return templates.TemplateResponse("index.html", {"request": request, "id": id, "name": data['name'], "value": data['value']})
        #return {"lol": data}
        # with Session() as session:
        #     response = get_task(id, session)
        #     templates = Jinja2Templates(directory='C:\\Users\\AdminIS\\micreservice\\templates')
        #     return templates.TemplateResponse("index.html", {"request": request, "id": id, "name": response['name'], "value": response['value']})

    else:
        raise HTTPException(status_code=404, detail="Data not found")


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
        o = Users(login=user.login, token=user.token)
        return create_user(o, session)


@app.post('/{resource_id}')
async def resource(id:int, user: Userr):
    resources = Resource(id=id, role_require='admin')
    if check_permission(user, resources):
        return {"message": "success"}
    return {"message": "forbidden"}


#@cached
@app.get('/{id}',  response_class=HTMLResponse)
async def render(request: Request, id: int):
    # dict = {"id": id}
    # enviroment = Environment(loader=FileSystemLoader("C:\\Users\\AdminIS\\micreservice\\templates"))
    # template = enviroment.get_template("index.html")
    with Session() as session:
        response = get_task_id(id, session)
        templates = Jinja2Templates(directory='C:\\Users\\AdminIS\\micreservice\\templates')
        return templates.TemplateResponse("index.html", {"request": request, "id": id, "name": response['name'], "value":response['value']})


if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)