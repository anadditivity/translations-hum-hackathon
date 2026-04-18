CREATE TABLE TRANSLATIONS (
	id SERIAL PRIMARY KEY,
	author int,
	translator int,
	editor int,
	comment_author int,
	title varchar(255) NOT NULL,
	title_original varchar(255),
	genre int,
	source_language int,
	source_literature int,
	publisher int,
	publication_location int,
	publication_year int NOT NULL,
	physical_description varchar(255),
	series int,
	publication_type int,
	target_audience int,
	print_number varchar(255),
	n_pages varchar(64),
	content varchar(255),
	issue varchar(255)
);

CREATE TABLE REVIEWS (
	id SERIAL PRIMARY KEY,
	translation_id int,
	author int,
	translator int,
	editor int,
	comment_author int,
	title varchar(255) NOT NULL,
	title_original varchar(255),
	genre int,
	source_language int,
	source_literature int,
	publisher int,
	publication_location int,
	publication_year int NOT NULL,
	physical_description varchar(255),
	series int,
	publication_type int,
	target_audience int,
	print_number varchar(255),
	n_pages varchar(255),
	content varchar(255),
	issue varchar(255)
); -- future work: review table should not contain data on translated book, that should be in translations

CREATE TABLE PERSONS (
	id SERIAL PRIMARY KEY,
	birth_year int,
	death_year int
);

CREATE TABLE NAMES (
	person_id int,
	language_id int,
	first_name varchar(255),
	last_name varchar(255)
);

CREATE TABLE LANGUAGES (
	id SERIAL PRIMARY KEY,
	est varchar(255),
	eng varchar (255)
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

CREATE TABLE PUBLISHERS (
	id SERIAL PRIMARY KEY,
	name varchar(255)
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

-- Intermediary tables

-- Translations
CREATE TABLE TRANSLATIONS_AUTHOR_PERSONS (
    translation_id int NOT NULL,
    person_id int NOT NULL
);

CREATE TABLE TRANSLATIONS_TRANSLATOR_PERSONS (
    translation_id int NOT NULL,
    person_id int NOT NULL
);

CREATE TABLE TRANSLATIONS_EDITOR_PERSONS (
    translation_id int NOT NULL,
    person_id int NOT NULL
);

CREATE TABLE TRANSLATIONS_COMMENT_PERSONS (
    translation_id int NOT NULL,
    person_id int NOT NULL
);

CREATE TABLE TRANSLATIONS_LANGUAGES (
    translation_id int NOT NULL,
    language_id int NOT NULL
);

CREATE TABLE TRANSLATIONS_GENRES (
    translation_id int NOT NULL,
    language_id int NOT NULL
);

CREATE TABLE TRANSLATIONS_LITERATURES (
    translation_id int NOT NULL,
    language_id int NOT NULL
);


CREATE TABLE TRANSLATIONS_LOCATIONS (
    translation_id int NOT NULL,
    language_id int NOT NULL
);

CREATE TABLE TRANSLATIONS_PUBLICATION_TYPES (
    translation_id int NOT NULL,
    language_id int NOT NULL
);

--- Reviews
CREATE TABLE REVIEWS_AUTHOR_PERSONS (
    review_id int NOT NULL,
    person_id int NOT NULL
);

CREATE TABLE REVIEWS_TRANSLATOR_PERSONS (
    review_id int NOT NULL,
    person_id int NOT NULL
);

CREATE TABLE REVIEWS_EDITOR_PERSONS (
    review_id int NOT NULL,
    person_id int NOT NULL
);

CREATE TABLE REVIEWS_COMMENT_PERSONS (
    review_id int NOT NULL,
    person_id int NOT NULL
);

CREATE TABLE REVIEWS_LANGUAGES (
    review_id int NOT NULL,
    language_id int NOT NULL
);

CREATE TABLE REVIEWS_GENRES (
    review_id int NOT NULL,
    language_id int NOT NULL
);

CREATE TABLE REVIEWS_LITERATURES (
    review_id int NOT NULL,
    language_id int NOT NULL
);

CREATE TABLE REVIEWS_LOCATIONS (
    review_id int NOT NULL,
    language_id int NOT NULL
);

CREATE TABLE REVIEWS_PUBLICATION_TYPES (
    review_id int NOT NULL,
    language_id int NOT NULL
);
