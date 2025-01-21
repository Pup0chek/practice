import fastapi
from fastapi import FastAPI
import uvicorn
from oauth import authorization_url


app = FastAPI()


@app.get('/')
def main_page():
    return fastapi.responses.RedirectResponse(authorization_url)




if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)