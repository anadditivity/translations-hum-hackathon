from pydantic import BaseModel

class TranslationItem(BaseModel):
    title: str
    author_first_name: str
    author_last_name: str
    author_birth_year: int
    author_death_year: str
    title_original:str
    translator_first_name:str
    translator_last_name:str
    translator_birth_year:str
    translator_death_year:str
    editor_first_name:str
    editor_last_name:str
    editor_birth_year:str
    editor_death_year:str
    publication_year:str
    source_language:str
    source_literature:str
    publication_location:str
    publisher:str
    series:str
    genre:str
    fore_afterword_author_first_name:str
    fore_afterword_author_last_name:str
    fore_afterword_author_birth_year:str
    fore_afterword_author_death_year:str
    edition:str
    publication_type:str
    target_audience:str
    issue: str
    notes:str
    n_pages:str
    content:str
    physical_description:str
    entry_lang: str

