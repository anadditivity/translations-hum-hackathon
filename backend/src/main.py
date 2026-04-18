from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware, #ty: ignore
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def query_traditional(
    title: str, author: str, title_original:str, translator:str,
    publication_year:str, source_language:str, source_literature:str,
    publication_location:str, publisher:str, series:str, genre:str,
    edition:str, fore_afterword_author:str, publication_type:str,
    target_audience:str
    ) -> dict[str, list]:
    return {"response": [{"title": "xd"}]}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

