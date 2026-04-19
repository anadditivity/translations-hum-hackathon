# HUM Hackathon April 2026 - Puzzled Maniacs - Estonian Translation Database
## Kristýna Bednářová, András Borbély, Maare Karmen Oras, Adeline Talvik

The repository for team Puzzled Maniacs for the HUM Hackathon 2026, working on the project "Estonian Translation Database". Initial overview of the database is [here](https://www.etkad.ee/humal/the-estonian-translation-database/).


# Data collection
The data was collected piecewise from the Tallinn University translations database [here](https://kirjandus.tlulib.ee/en/translated-estonian-literature-database/). Exporting was done in the following pieces:
- publication year: from 1900 to 1920.
- publication year: from 1921 to 1950.
- publication year: from 1951 to 2000.
- publication year: from 2001 to `_`.
The files were then simply concatenated, after removing the column row.


# Data processing pipeline
The data was processed both using R Markdown and Jupyter Notebooks. Check out installation information respectively for RStudio (https://posit.co/download/rstudio-desktop) and for Jupyter Notebook (https://jupyter.org/install).

The data was processed as follows to make it fit to the designed database structure:
1. `data/addy-exploding-data.ipynb`: a Jupyter Notebook file that splits the majority of rows from separator values. This ensures that we retain database good practices (first normal form). It saves the data into `data/exploded_data.csv`.
2. `data/data_processing_pipeline.Rmd`: an R Markdown file that contains the vast majority of data processing:
    - renames columns from Estonian to English;
    - fixes a ton of typos;
    - splits values into separate rows on the "unexpected" separators;
    - standardizes values in the columns.
The output is exported to `data/processed_translation_data_4.csv`.
3. `data/addy-data-to-db-structure.ipynb`: a Jupyter Notebook file that splits the processed data into the necessary structure for the database; main changes include:
    - splitting `author` into `first_name`, `last_name`, `birth_year`, `death_year` as well as possible. **This process may contain mistakes and should be re-checked.**
    - splitting the processed data into separate files `data/clean_for_sql/{genres,languages,literatures,locations,persons,publication_types,publishers,series,target_audiences,translations}.csv` for convenient importing into SQL.



# Technical setup
The front-end utilizes Python Flask: due to time limitations, this is not fully implemented. The database is based on PostgreSQL and runs in a separate Docker container.

Prerequisites:
- Docker (Linux: https://docs.docker.com/engine/install/, Windows: https://docs.docker.com/desktop/setup/install/windows-install/)


In theory, everything should set up with the `backend/docker-compose.yaml` file.
This requires a file `.env` with the credentials. It looks like this:
```
POSTGRES_USER=dbuser
POSTGRES_PASSWORD=...
```

On Linux CLI, this can be done with `docker compose up --build`; in Docker Desktop, you need to utilize the Docker Terminal in the bottom, do `cd backend/` and `docker compose up --build`. This will create a bunch of scary lines.

This should start the following services:
- PostgreSQL on `localhost:5432`.
- the main database interfacing API on `localhost:8000`
- Adminer for SQL on `localhost:8080`.

