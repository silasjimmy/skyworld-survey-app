# Simple Survey API

## Tools

- [Flask](https://flask.palletsprojects.com/en/stable/)
- [Postgres](https://www.postgresql.org/)

## Project Setup

### Development

1. Create a Postgres database locally and name it `sky_survey_db`
2. Create a `.env` file in the root directory and add the following environment variables:

```
DATABASE_USERNAME=<your_database_username>
DATABASE_PASSWORD=<your_database_password>
DATABASE_NAME=sky_survey_db
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

3. Create a virtual environment and activate it

4. Install the dependencies by running

```sh
pip install -r requirements.txt
```

5. Initialize the database by running the following commands:

```sh
flask db init
flask db migrate
flask db upgrade
```

6. On the root directory, create a new file and name it `.flaskenv`. Add the following flask environment variables to the file:

```
FLASK_APP=flaskr
FLASK_DEBUG=True
```

7. Run the following command to start the server:

```sh
flask run
```

### SQL Script Generation

Run the following command in the terminal (Linux distributions)

```sh
pg_dump -U postgres -d sky_survey_db --password -f sky_survey_db.sql
```
