from pydantic import BaseModel, field_validator
from typing import Optional

class TranslationItem(BaseModel):
    title: str
    author_first_name: str
    author_last_name: str
    author_birth_year: Optional[int] = None
    author_death_year: Optional[int] = None
    title_original: str
    translator_first_name: str
    translator_last_name: str
    translator_birth_year: Optional[int] = None
    translator_death_year: Optional[int] = None
    editor_first_name: str
    editor_last_name: str
    editor_birth_year: Optional[int] = None
    editor_death_year: Optional[int] = None
    publication_year: Optional[int] = None
    source_language: str
    source_literature: str
    publication_location: str
    publisher: str
    series: str
    genre: str
    fore_afterword_author_first_name: str
    fore_afterword_author_last_name: str
    fore_afterword_author_birth_year: Optional[int] = None
    fore_afterword_author_death_year: Optional[int] = None
    edition: str
    publication_type: str
    target_audience: str
    issue: str
    notes: str
    n_pages: Optional[int] = None
    content: str
    physical_description: str
    entry_lang: str

    @field_validator(
        "author_birth_year", "author_death_year",
        "translator_birth_year", "translator_death_year",
        "editor_birth_year", "editor_death_year",
        "publication_year", "fore_afterword_author_birth_year",
        "fore_afterword_author_death_year", "n_pages",
        mode="before"
    )
    @classmethod
    def empty_str_to_none(cls, v):
        if v == "" or v is None:
            return None
        return int(v)
