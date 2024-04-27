from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI, Query
from fastapi.routing import APIRouter
from api.routes import user_router
from api.login_route import login_router
from db import db_config_milvus

from fastapi.routing import APIRouter

from starlette.responses import PlainTextResponse, JSONResponse, HTMLResponse
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles



app = FastAPI(title="super-puper-site") 

main_api_router = APIRouter()

main_page = Jinja2Templates(directory="templates")

# Mount static files at "/static" path
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class = HTMLResponse)
async def index(request: Request):
    return main_page.TemplateResponse("new_index.html", {"request": request})

@app.get("/user_cabinet", response_class = HTMLResponse)
async def index(request: Request):
    return main_page.TemplateResponse("user_cab.html", {"request": request})

main_api_router.include_router(user_router, prefix="/user", tags=["user"])
main_api_router.include_router(login_router, prefix="/login", tags=["login"])

app.include_router(main_api_router)

@app.on_event("startup")
def init_vector_db():
    db_config_milvus.create_collections_if_not_exist(db_config_milvus.connection, "cluster")

