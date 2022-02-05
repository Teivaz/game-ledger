To run locally

1. Start a postgres db with 
```
docker run -d -p 5432:5432 -e POSTGRES_DB=game-ledger -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin postgres:9.6
```

2. Create necessary tables for the database using commands from the "backend/game_ledger/resources/tables.sql" file.

3. Install dependencies with `poetry install`

4. Activate virtual environment with `poetry shell`

5. Run the app with
```
FLASK_ENV=development FLASK_APP=game_ledger python -m flask run
```
