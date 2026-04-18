from fastapi import FastAPI, Depends
from db import engine, get_session
from contextlib import asynccontextmanager
from sqlmodel import SQLModel

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

@app.get("/")
async def read_root(session=Depends(get_session)):
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
