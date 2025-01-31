from sqlalchemy.sql.functions import user
from starlette.middleware.cors import CORSMiddleware
from api import router
from database import engine
from database import Base
from fastapi import FastAPI

Base.metadata.create_all(engine)

app = FastAPI(title="GJB")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router,prefix="/api")