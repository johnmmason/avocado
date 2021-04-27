# avocado/database

The database is automatically created by `docker_compose` while launching the project.

The schema is defined in `schema.sql`, which loads data from `avocado.csv`.

## Tables

### Avocado

| column_name | datatype    | description |
| ----------- | ----------- | ----------- |
| id          | SERIAL      | PRIMARY KEY |
| week_id     | INTEGER     | 0-51 where 51 is the first week of the year
| week        | DATE        | The first day of the week
| price       | REAL        | TW average price
| volume      | REAL        | TW sales
| total_4046  | REAL        | TW sales of PLU 4046
| total_4225  | REAL        | TW sales of PLU 4225
| total_4770  | REAL        | TW sales of PLU 4770
| category    | VARCHAR(20) | { conventional, organic }
| year        | INTEGER     |             |
| region      | VARCHAR(20) |             |
