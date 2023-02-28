from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI, Query
from fastapi.routing import APIRouter
from api.routes import user_router
from api.login_route import login_router


app = FastAPI(title="super-puper-site") 


main_api_router = APIRouter()

main_api_router.include_router(user_router, prefix="/user", tags=["user"])
main_api_router.include_router(login_router, prefix="/login", tags=["login"])
app.include_router(main_api_router)

