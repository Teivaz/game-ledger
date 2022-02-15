### To run locally

1. Start a postgres db with

```
docker run -d -p 5432:5432 -e POSTGRES_DB=game-ledger -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin postgres:9.6
```


2. Create necessary tables for the database using commands from the "backend/game_ledger/resources/tables.sql" file.
_Note_ on MacOS you need to have postgress installed prior to installing dependencies. To do so run `brew install postgresql`.
3. Install dependencies with `poetry install`
4. Activate virtual environment with `poetry shell`
5. Run the app with

```
FLASK_ENV=development FLASK_APP=game_ledger python -m flask run
```

### To create user

1. Run the app
2. Send POST request to "/api/user/register/" with body `{"name": "tester", "email": "test"}` and header `Content-Type=application/json`
3. In the app logs look for the token
4. Send GET request to "/api/user/register/" with `token` arg containing the found token. This will set correct cookies in the response so following requests will be authorised
