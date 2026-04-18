from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.src.crud import get_resource, create_resource

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
    ) -> list[dict[str, list]]:

        crud_input = {}
        for key, value in locals().items():
            if value is not None:
                crud_input[key] = value

        result = await get_resource(crud_input)

        return result

@app.post("/")
async def create_datapoint_traditional(
    title: str, author_first_name: str, author_last_name: str,
    author_birth_year: int,  author_death_year: str, title_original:str,
    translator_first_name:str, translator_last_name:str, translator_birth_year:str, translator_death_year:str,
    editor_first_name:str, editor_last_name:str, editor_birth_year:str, editor_death_year:str,
    publication_year:str, source_language:str, source_literature:str,
    publication_location:str, publisher:str, series:str, genre:str,
    fore_afterword_author_first_name:str, fore_afterword_author_last_name:str,
    fore_afterword_author_birth_year:str, fore_afterword_author_death_year:str,
    edition:str, publication_type:str, target_audience:str, # enums should have a dropdown menu (just publication type is enough)
    issue: str, notes:str, n_pages:str, content:str, physical_description:str,
    ) -> dict[str, list]:

    result = await create_resource(title, author_first_name, author_last_name, author_birth_year, author_death_year,
                    title_original, translator_first_name, translator_last_name, translator_birth_year,
                    translator_death_year, editor_first_name, editor_last_name, editor_birth_year, editor_death_year,
                    publication_year, source_language, source_literature, publication_location, publisher, series,
                    genre, fore_afterword_author_first_name, fore_afterword_author_last_name,
                    fore_afterword_author_birth_year, fore_afterword_author_death_year, edition, publication_type,
                    target_audience, issue, notes, n_pages, content, physical_description
    )

    return result

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

