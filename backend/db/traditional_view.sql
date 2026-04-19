CREATE OR REPLACE VIEW vw_translation_full AS
SELECT
    t.id,
    t.title,
    t.title_original,
    t.publication_year,
    t.physical_description,
    t.edition,
    t.n_pages,
    t.content,
    t.issue,
    t.notes,

    pub.name AS publisher,
    s.name AS series,
    ta.eng AS target_audience,

    /* authors */
    (
        SELECT string_agg(
            trim(
                coalesce(n.last_name, '') ||
                CASE
                    WHEN n.last_name IS NOT NULL AND n.first_name IS NOT NULL THEN ', '
                    ELSE ''
                END ||
                coalesce(n.first_name, '')
            ),
            '; '
            ORDER BY n.last_name, n.first_name
        )
        FROM TRANSLATIONS_AUTHOR_PERSONS tap
        JOIN NAMES n ON n.person_id = tap.person_id
        WHERE tap.translation_id = t.id
    ) AS author_names,

    (
        SELECT string_agg(
            trim(
                coalesce(n.last_name, '') ||
                CASE
                    WHEN n.last_name IS NOT NULL AND n.first_name IS NOT NULL THEN ', '
                    ELSE ''
                END ||
                coalesce(n.first_name, '')
            ),
            '; '
            ORDER BY n.last_name, n.first_name
        )
        FROM TRANSLATIONS_TRANSLATOR_PERSONS ttp
        JOIN NAMES n ON n.person_id = ttp.person_id
        WHERE ttp.translation_id = t.id
    ) AS translator_names,

    (
        SELECT string_agg(
            trim(
                coalesce(n.last_name, '') ||
                CASE
                    WHEN n.last_name IS NOT NULL AND n.first_name IS NOT NULL THEN ', '
                    ELSE ''
                END ||
                coalesce(n.first_name, '')
            ),
            '; '
            ORDER BY n.last_name, n.first_name
        )
        FROM TRANSLATIONS_EDITOR_PERSONS tep
        JOIN NAMES n ON n.person_id = tep.person_id
        WHERE tep.translation_id = t.id
    ) AS editor_names,

    (
        SELECT string_agg(
            trim(
                coalesce(n.last_name, '') ||
                CASE
                    WHEN n.last_name IS NOT NULL AND n.first_name IS NOT NULL THEN ', '
                    ELSE ''
                END ||
                coalesce(n.first_name, '')
            ),
            '; '
            ORDER BY n.last_name, n.first_name
        )
        FROM TRANSLATIONS_FORE_AFTERWORD_PERSONS tfp
        JOIN NAMES n ON n.person_id = tfp.person_id
        WHERE tfp.translation_id = t.id
    ) AS fore_afterword_author_names,

    /* years */
    (
        SELECT string_agg(coalesce(p.birth_year::text, ''), '; ')
        FROM TRANSLATIONS_AUTHOR_PERSONS tap
        JOIN PERSONS p ON p.id = tap.person_id
        WHERE tap.translation_id = t.id
    ) AS author_birth_years,

    (
        SELECT string_agg(coalesce(p.death_year::text, ''), '; ')
        FROM TRANSLATIONS_AUTHOR_PERSONS tap
        JOIN PERSONS p ON p.id = tap.person_id
        WHERE tap.translation_id = t.id
    ) AS author_death_years,

    /* languages */
    (
        SELECT string_agg(coalesce(l.eng, l.est), '; ' ORDER BY coalesce(l.eng, l.est))
        FROM TRANSLATIONS_LANGUAGES tl
        JOIN LANGUAGES l ON l.id = tl.language_id
        WHERE tl.translation_id = t.id
    ) AS source_language,

    /* literatures */
    (
        SELECT string_agg(coalesce(lit.eng, lit.est), '; ' ORDER BY coalesce(lit.eng, lit.est))
        FROM TRANSLATIONS_LITERATURES tlit
        JOIN LITERATURES lit ON lit.id = tlit.literature_id
        WHERE tlit.translation_id = t.id
    ) AS source_literature,

    /* locations */
    (
        SELECT string_agg(loc.name, '; ' ORDER BY loc.name)
        FROM TRANSLATIONS_LOCATIONS tloc
        JOIN LOCATIONS loc ON loc.id = tloc.location_id
        WHERE tloc.translation_id = t.id
    ) AS publication_location,

    /* genres */
    (
        SELECT string_agg(coalesce(g.eng, g.est), '; ' ORDER BY coalesce(g.eng, g.est))
        FROM TRANSLATIONS_GENRES tg
        JOIN GENRES g ON g.id = tg.genre_id
        WHERE tg.translation_id = t.id
    ) AS genre,

    /* publication types */
    (
        SELECT string_agg(coalesce(pt.eng, pt.est), '; ' ORDER BY coalesce(pt.eng, pt.est))
        FROM TRANSLATIONS_PUBLICATION_TYPES tpt
        JOIN PUBLICATION_TYPES pt ON pt.id = tpt.publication_type_id
        WHERE tpt.translation_id = t.id
    ) AS publication_type

FROM TRANSLATIONS t
LEFT JOIN PUBLISHERS pub ON pub.id = t.publisher
LEFT JOIN SERIES s ON s.id = t.series
LEFT JOIN TARGET_AUDIENCES ta ON ta.id = t.target_audience
WHERE EXISTS (SELECT 1 FROM TRANSLATIONS t2 WHERE t2.id = t.id);
