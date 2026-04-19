import pandas as pd
from db import engine
from sqlalchemy import text

# AI GENERATED CODE AHEAD

def get_or_create(conn, table, column, value):
    if pd.isna(value) or value == "":
        return None
    res = conn.execute(
        text(f"SELECT id FROM {table} WHERE {column} = :val"),
        {"val": value}
    ).fetchone()
    if res:
        return res[0]
    res = conn.execute(
        text(f"INSERT INTO {table} ({column}) VALUES (:val) RETURNING id"),
        {"val": value}
    ).fetchone()
    return res[0]


def parse_person(raw):
    if pd.isna(raw):
        return None

    raw = raw.strip()

    try:
        name_part, years = raw.rsplit(" ", 1)
        last, first = [x.strip() for x in name_part.split(",", 1)]
        birth, death = years.split("-")
        birth = int(birth) if birth else None
        death = int(death) if death else None
    except:
        return {
            "first_name": None,
            "last_name": raw,
            "birth_year": None,
            "death_year": None
        }

    return {
        "first_name": first,
        "last_name": last,
        "birth_year": birth,
        "death_year": death
    }


def get_or_create_person(conn, person_dict, language_id=1):
    if not person_dict:
        return None

    res = conn.execute(text("""
        SELECT p.id
        FROM PERSONS p
        JOIN NAMES n ON n.person_id = p.id
        WHERE n.first_name IS NOT DISTINCT FROM :first
        AND n.last_name = :last
        AND p.birth_year IS NOT DISTINCT FROM :birth
        AND p.death_year IS NOT DISTINCT FROM :death
        LIMIT 1
    """), {
        "first": person_dict["first_name"],
        "last": person_dict["last_name"],
        "birth": person_dict["birth_year"],
        "death": person_dict["death_year"]
    }).fetchone()

    if res:
        return res[0]

    pid = conn.execute(text("""
        INSERT INTO PERSONS (birth_year, death_year)
        VALUES (:birth, :death)
        RETURNING id
    """), {
        "birth": person_dict["birth_year"],
        "death": person_dict["death_year"]
    }).fetchone()[0]

    conn.execute(text("""
        INSERT INTO NAMES (person_id, language_id, first_name, last_name)
        VALUES (:pid, :lang, :first, :last)
    """), {
        "pid": pid,
        "lang": language_id,
        "first": person_dict["first_name"],
        "last": person_dict["last_name"]
    })

    return pid


def insert_m2m(conn, table, col1, col2, id1, id2):
    if not id1 or not id2:
        return
    conn.execute(text(f"""
        INSERT INTO {table} ({col1}, {col2})
        VALUES (:id1, :id2)
        ON CONFLICT DO NOTHING
    """), {"id1": id1, "id2": id2})


# --- LOAD SIMPLE TABLES ---

def load_simple_table(csv_file, table, column):
    df = pd.read_csv(csv_file)
    with engine.begin() as conn:
        for _, row in df.iterrows():
            get_or_create(conn, table, column, row[column])


load_simple_table("../../data/clean_for_sql/genres.csv", "GENRES", "est")
load_simple_table("../../data/clean_for_sql/languages.csv", "LANGUAGES", "est")
load_simple_table("../../data/clean_for_sql/literature.csv", "LITERATURES", "est")
load_simple_table("../../data/clean_for_sql/publication_types.csv", "PUBLICATION_TYPES", "est")
load_simple_table("../../data/clean_for_sql/target_audiences.csv", "TARGET_AUDIENCES", "est")

load_simple_table("../../data/clean_for_sql/locations.csv", "LOCATIONS", "name")
load_simple_table("../../data/clean_for_sql/publishers.csv", "PUBLISHERS", "name")
load_simple_table("../../data/clean_for_sql/series.csv", "SERIES", "name")


# --- LOAD TRANSLATIONS ---

df = pd.read_csv("../../data/clean_for_sql/translations.csv")

with engine.begin() as conn:
    for _, row in df.iterrows():

        publisher_id = get_or_create(conn, "PUBLISHERS", "name", row["publisher"])
        series_id = get_or_create(conn, "SERIES", "name", row["series"])
        target_id = get_or_create(conn, "TARGET_AUDIENCES", "est", row["target_audience"])

        translation_id = conn.execute(text("""
            INSERT INTO TRANSLATIONS (
                title, title_original, publisher, publication_year,
                physical_description, series, target_audience,
                edition, n_pages, content, issue, notes
            ) VALUES (
                :title, :title_original, :publisher, :year,
                :phys, :series, :target,
                :edition, :pages, :content, :issue, :notes
            ) RETURNING id
        """), {
            "title": row["title"],
            "title_original": row["title_original"],
            "publisher": publisher_id,
            "year": row["publication_year"],
            "phys": row["physical_description"],
            "series": series_id,
            "target": target_id,
            "edition": row["edition"],
            "pages": row["n_pages"],
            "content": row["content"],
            "issue": row["issue"],
            "notes": row["notes"]
        }).fetchone()[0]

        # --- PERSON ROLES ---
        roles = {
            "author": "TRANSLATIONS_AUTHOR_PERSONS",
            "translator": "TRANSLATIONS_TRANSLATOR_PERSONS",
            "editor": "TRANSLATIONS_EDITOR_PERSONS",
            "fore_afterword_author": "TRANSLATIONS_FORE_AFTERWORD_PERSONS"
        }

        for col, table in roles.items():
            persons = str(row[col]).split(";") if pd.notna(row[col]) else []
            for p in persons:
                pdata = parse_person(p)
                pid = get_or_create_person(conn, pdata)
                insert_m2m(conn, table, "translation_id", "person_id", translation_id, pid)

        # --- GENRES ---
        genre_id = get_or_create(conn, "GENRES", "est", row["genre"])
        insert_m2m(conn, "TRANSLATIONS_GENRES", "translation_id", "genre_id", translation_id, genre_id)

        # --- LANGUAGE ---
        lang_id = get_or_create(conn, "LANGUAGES", "est", row["source_language"])
        insert_m2m(conn, "TRANSLATIONS_LANGUAGES", "translation_id", "language_id", translation_id, lang_id)

        # --- LITERATURE ---
        lit_id = get_or_create(conn, "LITERATURES", "est", row["source_literature"])
        insert_m2m(conn, "TRANSLATIONS_LITERATURES", "translation_id", "literature_id", translation_id, lit_id)

        # --- LOCATION ---
        loc_id = get_or_create(conn, "LOCATIONS", "name", row["publication_location"])
        insert_m2m(conn, "TRANSLATIONS_LOCATIONS", "translation_id", "location_id", translation_id, loc_id)

        # --- PUBLICATION TYPE ---
        pub_type_id = get_or_create(conn, "PUBLICATION_TYPES", "est", row["publication_type"])
        insert_m2m(conn, "TRANSLATIONS_PUBLICATION_TYPES", "translation_id", "publication_type_id", translation_id, pub_type_id)
