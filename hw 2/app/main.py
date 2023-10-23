from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from starlette.responses import FileResponse
from app.db import create_tables
from app.routes.vote import router

import logging
logging.basicConfig(level=logging.WARNING)


app = FastAPI()

#favicon_path = 'favicon.ico'


@app.on_event("startup")
async def startup_event():
    await create_tables()


# @app.get('/db hw/favicon.ico', include_in_schema=False)
# async def favicon():
#     return FileResponse(favicon_path)


@app.get("/", include_in_schema=False)
def startup_page():
    return "db hw 2"


@app.get("/docs", include_in_schema=False)
def overridden_swagger():
    return get_swagger_ui_html(openapi_url="openapi.json",
                               title="db hw 2",
                               swagger_favicon_url="/db hw 2/favicon.ico")


# @app.get("/redoc", include_in_schema=False)
# def overridden_redoc():
#     return get_redoc_html(openapi_url="/db_hw/openapi.json", title="db hw",
#                           redoc_favicon_url="/db_hw/favicon.ico")


app.include_router(router, prefix='/db_hw_2', tags=['db hw 2'])

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
