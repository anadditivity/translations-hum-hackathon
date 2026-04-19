CREATE TABLE PUBLISHERS(
	id SERIAL PRIMARY KEY,
	name varchar(255)
);

CREATE TABLE SERIES (
	id SERIAL PRIMARY KEY,
	name varchar(255)
);

CREATE TABLE TARGET_AUDIENCES (
	id SERIAL PRIMARY KEY,
	est varchar(255),
	eng varchar(255)
);

CREATE TABLE LANGUAGES (
	id SERIAL PRIMARY KEY,
	est varchar(255),
	eng varchar (255)
);


CREATE TABLE GENRES (
	id SERIAL PRIMARY KEY,
	est varchar(255),
	eng varchar(255)
);

CREATE TABLE LITERATURES (
	id SERIAL PRIMARY KEY,
	est varchar(255),
	eng varchar(255)
);

CREATE TABLE LOCATIONS (
	id SERIAL PRIMARY KEY,
	name varchar(255)
);


CREATE TABLE PUBLICATION_TYPES (
	id SERIAL PRIMARY KEY,
	est varchar(255),
	eng varchar(255)
);

CREATE TABLE TRANSLATIONS (
	id SERIAL PRIMARY KEY,
	title varchar(255) NOT NULL,
	title_original varchar(255),
	publisher int, --fk
	publication_year int NOT NULL,
	physical_description varchar(255),
	series int, --fk
    target_audience int, --dk
	edition varchar(255),
	n_pages varchar(64),
	content varchar(255),
	issue varchar(255),
	notes varchar(255),

    CONSTRAINT fk_publisher
    FOREIGN KEY (publisher)
    REFERENCES PUBLISHERS(id),

    CONSTRAINT fk_series
    FOREIGN KEY (series)
    REFERENCES SERIES(id),

    CONSTRAINT fk_target_audience
    FOREIGN KEY (target_audience)
    REFERENCES TARGET_AUDIENCES(id)
);


CREATE TABLE PERSONS (
	id SERIAL PRIMARY KEY,
	birth_year int,
	death_year int
);

CREATE TABLE NAMES (
	person_id int, --fk
	language_id int, --fk
	first_name varchar(255),
	last_name varchar(255),

    CONSTRAINT fk_person_id
    FOREIGN KEY (person_id)
    REFERENCES PERSONS(id),

    CONSTRAINT fk_language_id
    FOREIGN KEY (language_id)
    REFERENCES LANGUAGES(id)
);


-- Intermediary tables

-- Translations
CREATE TABLE TRANSLATIONS_AUTHOR_PERSONS (
    translation_id int NOT NULL,
    person_id int NOT NULL,

    PRIMARY KEY (translation_id, person_id),

    CONSTRAINT fk_translation_id
    FOREIGN KEY (translation_id)
    REFERENCES TRANSLATIONS(id),

    CONSTRAINT fk_person_id
    FOREIGN KEY (person_id)
    REFERENCES PERSONS(id)
);

CREATE TABLE TRANSLATIONS_TRANSLATOR_PERSONS (
    translation_id int NOT NULL,
    person_id int NOT NULL,

    PRIMARY KEY (translation_id, person_id),

    CONSTRAINT fk_translation_id
    FOREIGN KEY (translation_id)
    REFERENCES TRANSLATIONS(id),

    CONSTRAINT fk_person_id
    FOREIGN KEY (person_id)
    REFERENCES PERSONS(id)
);

CREATE TABLE TRANSLATIONS_EDITOR_PERSONS (
    translation_id int NOT NULL,
    person_id int NOT NULL,

    PRIMARY KEY (translation_id, person_id),

    CONSTRAINT fk_translation_id
    FOREIGN KEY (translation_id)
    REFERENCES TRANSLATIONS(id),

    CONSTRAINT fk_person_id
    FOREIGN KEY (person_id)
    REFERENCES PERSONS(id)
);

CREATE TABLE TRANSLATIONS_FORE_AFTERWORD_PERSONS (
    translation_id int NOT NULL,
    person_id int NOT NULL,

    PRIMARY KEY (translation_id, person_id),

    CONSTRAINT fk_translation_id
    FOREIGN KEY (translation_id)
    REFERENCES TRANSLATIONS(id),

    CONSTRAINT fk_person_id
    FOREIGN KEY (person_id)
    REFERENCES PERSONS(id)
);

CREATE TABLE TRANSLATIONS_REVIEWED_BOOK_AUTHORS_PERSONS (
    translation_id int NOT NULL,
    person_id int NOT NULL,

    PRIMARY KEY (translation_id, person_id),

    CONSTRAINT fk_translation_id
    FOREIGN KEY (translation_id)
    REFERENCES TRANSLATIONS(id),

    CONSTRAINT fk_person_id
    FOREIGN KEY (person_id)
    REFERENCES PERSONS(id)
);

CREATE TABLE TRANSLATIONS_LANGUAGES (
    translation_id int NOT NULL,
    language_id int NOT NULL,

    PRIMARY KEY (translation_id, language_id),

    CONSTRAINT fk_translation_id
    FOREIGN KEY (translation_id)
    REFERENCES TRANSLATIONS(id),

    CONSTRAINT fk_languages_id
    FOREIGN KEY (language_id)
    REFERENCES LANGUAGES(id)
);

CREATE TABLE TRANSLATIONS_GENRES (
    translation_id int NOT NULL,
    genre_id int NOT NULL,

    PRIMARY KEY (translation_id, genre_id),

    CONSTRAINT fk_translation_id
    FOREIGN KEY (translation_id)
    REFERENCES TRANSLATIONS(id),

    CONSTRAINT fk_genre_id
    FOREIGN KEY (genre_id)
    REFERENCES GENRES(id)
);

CREATE TABLE TRANSLATIONS_LITERATURES (
    translation_id int NOT NULL,
    literature_id int NOT NULL,

    PRIMARY KEY (translation_id, literature_id),

    CONSTRAINT fk_translation_id
    FOREIGN KEY (translation_id)
    REFERENCES TRANSLATIONS(id),

    CONSTRAINT fk_literature_id
    FOREIGN KEY (literature_id)
    REFERENCES LITERATURES(id)
);

CREATE TABLE TRANSLATIONS_LOCATIONS (
    translation_id int NOT NULL,
    location_id int NOT NULL,

    PRIMARY KEY (translation_id, location_id),

    CONSTRAINT fk_translation_id
    FOREIGN KEY (translation_id)
    REFERENCES TRANSLATIONS(id),

    CONSTRAINT fk_location_id
    FOREIGN KEY (location_id)
    REFERENCES LOCATIONS(id)
);

CREATE TABLE TRANSLATIONS_PUBLICATION_TYPES (
    translation_id int NOT NULL,
    publication_type_id int NOT NULL,

    PRIMARY KEY (translation_id, publication_type_id),

    CONSTRAINT fk_translation_id
    FOREIGN KEY (translation_id)
    REFERENCES TRANSLATIONS(id),

    CONSTRAINT fk_publication_type_id
    FOREIGN KEY (publication_type_id)
    REFERENCES PUBLICATION_TYPES(id)
);
