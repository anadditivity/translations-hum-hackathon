CREATE TABLE TRANSLATIONS (
	id int AUTO_INCREMENT PRIMARY KEY,
	author int,
	translator int,
	editor int,
	comment_text_author int,
	title varchar(255) NOT NULL,
	title_original varchar(255),
	genre int,
	source_language int,
	source_literature int,
	publisher int,
	publication_location int,
	publication_year int(4) NOT NULL,
	physical_description varchar(255),
	series int,
	publication_type int,
	target_audience,
	edition varchar(255),
	n_pages varchar(64),
	content varchar(255),
	periodical_name varchar(255)
)

CREATE TABLE REVIEWS (
	id int AUTO_INCREMENT PRIMARY KEY,
	translation_id int,
	author int,
	translator int,
	editor int,
	...,
	title varchar(255) NOT NULL,
	title_original varchar(255),
	genre int,
	source_language int,
	source_literature int,
	publisher int,
	publication_location int,
	publication_year int(8) NOT NULL,
	physical_description varchar(255),
	series int,
	publication_type int,
	target_audience,
	edition varchar(255),
	n_pages varchar(255),
	content varchar(255),
	periodical_name varchar(255)
) -- future work: review table should not contain data on translated book, that should be in translations

CREATE TABLE PERSONS (
	id int AUTO_INCREMENT PRIMARY KEY,
	birth_year int(4),
	death_year int(4),
)

CREATE TABLE NAMES (
	person_id int,
	language_id int,
	first_name varchar(255),
	last_name varchar(255)
)

CREATE TABLE LANGUAGES (
	id int AUTO_INCREMENT PRIMARY KEY,
	est varchar(255),
	eng varchar (255)
)

CREATE TABLE SERIES (
	id int AUTO_INCREMENT PRIMARY KEY,
	name varchar(255)
)

CREATE TABLE TARGET_AUDIENCES (
	id int AUTO_INCREMENT PRIMARY KEY,
	est varchar(255),
	eng varchar(255)
)

CREATE TABLE GENRES (
	id int AUTO_INCREMENT PRIMARY KEY,
	est varchar(255),
	eng varchar(255)
)

CREATE TABLE LITERATURES (
	id int AUTO_INCREMENT PRIMARY KEY,
	est varchar(255),
	eng varchar(255)
)

CREATE TABLE PUBLISHERS (
	id int AUTO_INCREMENT PRIMARY KEY,
	name varchar(255)
)

CREATE TABLE LOCATIONS (
	id int AUTO_INCREMENT PRIMARY KEY,
	name varchar(255)
)

CREATE TABLE PUBLICATION_TYPES (
	id int AUTO_INCREMENT PRIMARY KEY,
	est varchar(255),
	eng varchar(255)
)
