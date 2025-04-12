# Simple survey API

## Tools

- [Flask](https://flask.palletsprojects.com/en/stable/)
- [Postgres](https://www.postgresql.org/)

## Setup

1. Create a Postgres database locally and name it `sky_survey_db`
2. Create a _.env_ file in the root directory and add the following environment variables:

```
DATABASE_USERNAME=<your_database_username>
DATABASE_PASSWORD=<your_database_password>
DATABASE_NAME=sky_survey_db
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

3. Create a virtual environment and activate it

4. Install the dependencies by running `pip install -r requirements.txt`

5. Initialize the database by running the following commands:

```
flask db init
flask db migrate
flask db upgrade
```

6. On the root directory, create a new file and name it _.flaskenv_. Add the following flask environment variables to the file:

```
FLASK_APP=flaskr
FLASK_DEBUG=True
```

7. Run the following command `flask run` to start the server.

## Development

- Generate SQL script: `pg_dump -U postgres -d sky_survey_db --password -f sky_survey_db.sql`
