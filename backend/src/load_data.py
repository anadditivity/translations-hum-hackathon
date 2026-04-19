import csv
import re
from sqlalchemy import text
from db import engine



# ---------- HELPERS ----------

def get_or_create(conn, table, column, value):
    if not value:
        return None

    result = conn.execute(
        text(f"SELECT id FROM {table} WHERE {column} = :val"),
        {"val": value}
    ).fetchone()

    if result:
        return result[0]

    result = conn.execute(
        text(f"INSERT INTO {table} ({column}) VALUES (:val) RETURNING id"),
        {"val": value}
    ).fetchone()

    return result[0]


def get_or_create_person(conn, first_name, last_name, birth_year, death_year):
    # 1) find person by core attributes (no names anymore)
    result = conn.execute(text("""
        SELECT id FROM persons
        WHERE birth_year IS NOT DISTINCT FROM :by
          AND death_year IS NOT DISTINCT FROM :dy
    """), {
        "by": birth_year,
        "dy": death_year
    }).fetchone()

    if result:
        person_id = result[0]
    else:
        result = conn.execute(text("""
            INSERT INTO persons (birth_year, death_year)
            VALUES (:by, :dy)
            RETURNING id
        """), {
            "by": birth_year,
            "dy": death_year
        }).fetchone()

        person_id = result[0]

    # 2) insert/update names in separate table
    if first_name or last_name:
        existing = conn.execute(text("""
            SELECT 1 FROM names
            WHERE person_id = :pid
              AND language_id = (SELECT id from LANGUAGES where est = 'est' or est = 'eesti')
        """), {"pid": person_id}).fetchone()

        if not existing:
            conn.execute(text("""
                INSERT INTO names (person_id, language_id, first_name, last_name)
                VALUES (:pid, (SELECT id from LANGUAGES where est = 'est' or est = 'eesti'), :fn, :ln)
            """), {
                "pid": person_id,
                "fn": first_name,
                "ln": last_name
            })

    return person_id


def parse_person(conn, raw):
    if not raw or raw.strip() == "":
        return None

    raw = raw.strip()

    match = re.match(r"^(.*?),\s*(.*?)\s*(\d{4})?-(\d{4})?$", raw)
    if match:
        last_name, first_name, birth, death = match.groups()
        return get_or_create_person(
            conn,
            first_name or None,
            last_name,
            int(float(birth)) if birth else None,
            int(float(death)) if death else None,
        )

    return get_or_create_person(conn, None, raw, None, None)


# ---------- LOAD SIMPLE TABLES ----------

def load_simple(file, table, column):
    with open(file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            value = row[column].strip()
            if value:
                get_or_create(conn, table, column, value)


with engine.begin() as conn:

    # est tables
    for file, table in [
        ("data/genres.csv", "genres"),
        ("data/languages.csv", "languages"),
        ("data/literatures.csv", "literatures"),
        ("data/publication_types.csv", "publication_types"),
        ("data/target_audiences.csv", "target_audiences"),
    ]:
        with open(file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                val = row["est"].strip()
                if val:
                    get_or_create(conn, table, "est", val)

    # name tables
    for file, table in [
        ("data/locations.csv", "locations"),
        ("data/publishers.csv", "publishers"),
        ("data/series.csv", "series"),
    ]:
        with open(file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                val = row["name"].strip()
                if val:
                    get_or_create(conn, table, "name", val)

    # persons.csv
    with open("data/persons.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            row = row['first_name,last_name,birth_year,death_year'].split(sep=',')
            get_or_create_person(
                conn,
                row[0],
                row[1],
                int(float(row[2])) if row[2] else None,
                int(float(row[3])) if row[3] else None,
            )

    # translations.csv
    with open("data/translations.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")

        for row in reader:

            author_id = parse_person(conn, row["author"])
            translator_id = parse_person(conn, row["translator"])
            editor_id = parse_person(conn, row["editor"])
            fore_id = parse_person(conn, row["fore_afterword_author"])

            genre_id = get_or_create(conn, "genres", "est", row["genre"])
            lang_id = get_or_create(conn, "languages", "est", row["source_language"])
            lit_id = get_or_create(conn, "literatures", "est", row["source_literature"])
            publisher_id = get_or_create(conn, "publishers", "name", row["publisher"])
            location_id = get_or_create(conn, "locations", "name", row["publication_location"])
            series_id = get_or_create(conn, "series", "name", row["series"])
            pubtype_id = get_or_create(conn, "publication_types", "est", row["publication_type"])
            audience_id = get_or_create(conn, "target_audiences", "est", row["target_audience"])

            conn.execute(text("""
                INSERT INTO translations (
                    title, title_original, publication_year,
                    physical_description, edition, n_pages,
                    content, issue, notes,
                    author, translator, editor, fore_afterword_author,
                    genre, source_language, source_literature,
                    publisher, publication_location, series,
                    publication_type, target_audience
                ) VALUES (
                    :title, :title_original, :year,
                    :phys, :edition, :pages,
                    :content, :issue, :notes,
                    :author, :translator, :editor, :fore,
                    :genre, :lang, :lit,
                    :publisher, :location, :series,
                    :pubtype, :audience
                )
            """), {
                "title": row["title"],
                "title_original": row["title_original"],
                "year": int(row["publication_year"]) if row["publication_year"] else None,
                "phys": row["physical_description"],
                "edition": row["edition"],
                "pages": int(row["n_pages"]) if row["n_pages"] else None,
                "content": row["content"],
                "issue": row["issue"],
                "notes": row["notes"],
                "author": author_id,
                "translator": translator_id,
                "editor": editor_id,
                "fore": fore_id,
                "genre": genre_id,
                "lang": lang_id,
                "lit": lit_id,
                "publisher": publisher_id,
                "location": location_id,
                "series": series_id,
                "pubtype": pubtype_id,
                "audience": audience_id,
            })
