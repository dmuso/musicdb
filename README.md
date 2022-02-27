# Music DB

## CSV Import Structures

### Field Order and Structure

| Column | Column Name               | Structure Notes                                                                                 | Example                       |
| :----: | :------------------------ | :---------------------------------------------------------------------------------------------- | :---------------------------- |
|   A    | Catalogue Number          | Instrument Abbreviation + Category Code . Increment Number . Volume                             | FL01.0001.01                  |
|   B    | Number of Copies          | A single number                                                                                 | 3                             |
|   C    | Instrument                | Instrument Name                                                                                 | Flute                         |
|   D    | Category                  | (Category Code) Name                                                                            | (05) Technical Work           |
|   E    | Grade                     | Number or range                                                                                 | 1 or 1-4                      |
|   F    | Title                     | Name of piece, free text                                                                        | Flute Series 1 - Fourth Grade |
|   G    | Accompaniment/Instruments | Comma separated list of instrument names                                                        | Piano, Drums, Bass Guitar     |
|   H    | Composer / Arranger       | Forward slash (/) separated list of composers, last name, then first name, separated by a comma | Cubbin, D./Rosser, Aaron      |
|   I    | Publisher                 | Publisher name, free text                                                                       | Allans Music                  |
|   J    | ISBN/Cat. No/Item No      | Code provided by the publisher, ISBN preferred, free text                                       | 1203051739                    |
|   K    | Missing Parts             | Free text                                                                                       | Copy 2 missing flute          |
|   L    | Location                  | Location name                                                                                   | SS Music 10                   |
|   M    | Date Last Checked         | Date in DD/MM/YYYY format                                                                       | 24/05/2021                    |
|   N    | Notes                     | Free text                                                                                       | Photocopies in Green folder   |


## Notes and Feature Requests

* Search by composer
* Add image of book
* Composer / Arranger or Editor, delimited by forward slash, teachers will search by arranger
* Arr. prefixes arranger
* Find catalogue numbers that are not used
* Add columns from Concert Band file
* Add barcode field
* Add notes by teacher
* Add/protect notes by library staff

## Common Commands

    # Generate migrations
    python manage.py makemigrations polls

    # Apply migrations
    python manage.py migrate

    # Console CLI
    python manage.py shell

## Infrastructure

DO Postgres: default db (defaultdb) and default admin user (doadmin)
