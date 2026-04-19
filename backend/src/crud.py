from db import engine
from sqlalchemy import select, insert, text
from sqlalchemy.engine import Connection
from trans_item import TranslationItem

# generic function for getting information the same way the original db did
async def get_resource(json: dict) -> list[dict]:
    with engine.connect() as con:
    
        # for key, value in json.items():
        #     ...

        result = con.execute(text('SELECT * FROM TRANSLATIONS;')).fetchall()

        result_dict = [dict(row) for row in result]
    result.append({
        "title": "dummy title",
        "author": "dummy author",
    })
    return result

async def create_resource(item: TranslationItem) -> str:
    conn = engine.connect()

    title = item.title 
    author_first_name = item.author_first_name 
    # author_last_name = item.author_last_name 
    author_birth_year = item.author_birth_year 
    # author_death_year = item.author_death_year 
    title_original = item.title_original 
    translator_first_name = item.translator_first_name 
    # translator_last_name = item.translator_last_name 
    translator_birth_year = item.translator_birth_year 
    # translator_death_year = item.translator_death_year 
    editor_first_name = item.editor_first_name 
    # editor_last_name = item.editor_last_name 
    editor_birth_year = item.editor_birth_year 
    # editor_death_year = item.editor_death_year 
    publication_year = item.publication_year 
    # source_language = item.source_language 
    # source_literature = item.source_literature 
    publication_location = item.publication_location 
    # publisher = item.publisher 
    # series = item.series 
    # genre = item.genre 
    fore_afterword_author_first_name = item.fore_afterword_author_first_name 
    # fore_afterword_author_last_name = item.fore_afterword_author_last_name 
    fore_afterword_author_birth_year = item.fore_afterword_author_birth_year 
    # fore_afterword_author_death_year = item.fore_afterword_author_death_year 
    edition = item.edition 
    # publication_type = item.publication_type 
    # target_audience = item.target_audience 
    issue = item.issue 
    # notes = item.notes 
    # n_pages = item.n_pages 
    # content = item.content 
    # physical_description = item.physical_description 
    entry_lang = item.entry_lang 

    result = await insert_translation(
        conn, title, author_first_name, author_birth_year, title_original,
        translator_first_name, translator_birth_year, editor_first_name,
        editor_birth_year, publication_year, publication_location,
        fore_afterword_author_first_name, fore_afterword_author_birth_year,
        edition, issue, entry_lang,
    )

    return result

### AI GENERATED CODE, bugs may be present
def get_or_create(conn: Connection, table: str, where_cols: dict, insert_cols: dict):
    row = conn.execute(
        select(table).filter_by(**where_cols)
    ).mappings().first()
    if row:
        return row

    result = conn.execute(
        insert(table).values(**insert_cols).returning(table)
    )
    return result.mappings().first()


def insert_translation(
    conn: Connection,
    title,
    author_first_name=None, author_last_name=None,
    author_birth_year=None, author_death_year=None,
    title_original=None,
    translator_first_name=None, translator_last_name=None,
    translator_birth_year=None, translator_death_year=None,
    editor_first_name=None, editor_last_name=None,
    editor_birth_year=None, editor_death_year=None,
    publication_year=None, source_language=None, source_literature=None,
    publication_location=None, publisher=None, series=None, genre=None,
    fore_afterword_author_first_name=None, fore_afterword_author_last_name=None,
    fore_afterword_author_birth_year=None, fore_afterword_author_death_year=None,
    edition=None, publication_type=None, target_audience=None,
    issue=None, notes=None, n_pages=None, content=None, physical_description=None,
    entry_lang=None,
):
    # --- lookup tables ---
    publisher_row = get_or_create(conn, PUBLISHERS, {"name": publisher}, {"name": publisher}) if publisher else None
    series_row = get_or_create(conn, SERIES, {"name": series}, {"name": series}) if series else None
    genre_row = get_or_create(conn, GENRES, {"eng": genre}, {"eng": genre}) if genre else None
    literature_row = get_or_create(conn, LITERATURES, {"eng": source_literature}, {"eng": source_literature}) if source_literature else None
    location_row = get_or_create(conn, LOCATIONS, {"name": publication_location}, {"name": publication_location}) if publication_location else None
    target_row = get_or_create(conn, TARGET_AUDIENCES, {"eng": target_audience}, {"eng": target_audience}) if target_audience else None
    pubtype_row = get_or_create(conn, PUBLICATION_TYPES, {"eng": publication_type}, {"eng": publication_type}) if publication_type else None
    source_lang_row = get_or_create(conn, LANGUAGES, {"eng": source_language}, {"eng": source_language, "est": source_language}) if source_language else None
    entry_lang_row = get_or_create(conn, LANGUAGES, {"eng": entry_lang}, {"eng": entry_lang, "est": entry_lang}) if entry_lang else None

    # --- persons ---
    def create_person(first, last, birth, death):
        if not (first or last):
            return None
        person = conn.execute(
            insert(PERSONS)
            .values(birth_year=birth, death_year=death)
            .returning(PERSONS)
        ).mappings().first()

        if entry_lang_row:
            conn.execute(
                insert(NAMES).values(
                    person_id=person["id"],
                    language_id=entry_lang_row["id"],
                    first_name=first,
                    last_name=last,
                )
            )
        return person

    author = create_person(author_first_name, author_last_name, author_birth_year, author_death_year)
    translator = create_person(translator_first_name, translator_last_name, translator_birth_year, translator_death_year)
    editor = create_person(editor_first_name, editor_last_name, editor_birth_year, editor_death_year)
    foreword = create_person(
        fore_afterword_author_first_name,
        fore_afterword_author_last_name,
        fore_afterword_author_birth_year,
        fore_afterword_author_death_year,
    )

    # --- translation ---
    translation = conn.execute(
        insert(TRANSLATIONS)
        .values(
            title=title,
            title_original=title_original,
            publisher=publisher_row["id"] if publisher_row else None,
            publication_year=publication_year,
            physical_description=physical_description,
            series=series_row["id"] if series_row else None,
            target_audience=target_row["id"] if target_row else None,
            edition=edition,
            n_pages=n_pages,
            content=content,
            issue=issue,
            notes=notes,
        )
        .returning(TRANSLATIONS)
    ).mappings().first()

    tid = translation["id"]

    # --- relations ---
    if author:
        conn.execute(insert(TRANSLATIONS_AUTHOR_PERSONS).values(translation_id=tid, person_id=author["id"]))
    if translator:
        conn.execute(insert(TRANSLATIONS_TRANSLATOR_PERSONS).values(translation_id=tid, person_id=translator["id"]))
    if editor:
        conn.execute(insert(TRANSLATIONS_EDITOR_PERSONS).values(translation_id=tid, person_id=editor["id"]))
    if foreword:
        conn.execute(insert(TRANSLATIONS_FORE_AFTERWORD_PERSONS).values(translation_id=tid, person_id=foreword["id"]))

    if source_lang_row:
        conn.execute(insert(TRANSLATIONS_LANGUAGES).values(translation_id=tid, language_id=source_lang_row["id"]))
    if genre_row:
        conn.execute(insert(TRANSLATIONS_GENRES).values(translation_id=tid, genre_id=genre_row["id"]))
    if literature_row:
        conn.execute(insert(TRANSLATIONS_LITERATURES).values(translation_id=tid, literature_id=literature_row["id"]))
    if location_row:
        conn.execute(insert(TRANSLATIONS_LOCATIONS).values(translation_id=tid, location_id=location_row["id"]))
    if pubtype_row:
        conn.execute(insert(TRANSLATIONS_PUBLICATION_TYPES).values(translation_id=tid, publication_type_id=pubtype_row["id"]))

    return "success"
