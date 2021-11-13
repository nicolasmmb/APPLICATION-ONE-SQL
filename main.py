from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
# ///
from app.configs.config import DatabaseConfig
# Routes
from app.routes import user, address, auth
from app.utils import endpoints


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth")
app.include_router(user.router, prefix="/api")
app.include_router(address.router, prefix="/api")
app.include_router(endpoints.router, prefix="/api")


# @app.get("/")
# def root():
#     return {"message": DatabaseConfig().get_url_connection()}
