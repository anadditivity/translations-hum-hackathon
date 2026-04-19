from trans_item import TranslationItem
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from crud import get_resource, create_resource

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/query_translation")
async def query_traditional(
    title: str, author: str, title_original:str, translator:str,
    publication_year_from:str, publication_year_to:str, source_language:str, source_literature:str,
    publication_location:str, publisher:str, series:str, genre:str,
    edition:str, fore_afterword_author:str, publication_type:str,
    target_audience:str, entry_lang:str,
    ) -> list[dict[str, str]]:

        crud_input = {}
        for key, value in locals().items():
            if value is not None:
                crud_input[key] = value

        result = await get_resource(crud_input)

        return result

@app.post("/upload_translation")
async def create_datapoint_traditional(item: TranslationItem) -> dict[str, list]:
    result = await create_resource(item)

    return result
