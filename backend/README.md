# backend

- install
  ```bash
  brew install pipx # install pipx.
  pipx install poetry # install poetry 
  brew install mysql # install mysql client.
  poetry self add poetry-plugin-shell
  poetry shell # activate virtual environment, if not already activated.
  poetry lock # update poetry.lock file
  poetry install # install dependencies.
  ```
- in `config` directory, create a .secrets.test.toml file and a .secrets.development.toml file with the following content:
  ```toml
  dynaconf_merge = true

  [MYSQL]
  username = "user"
  password = "password"
  ```
- Database Migration
  - login to the database container
    ```bash
    docker exec -it backend bash
    ```
  - create a new version
    ```bash
    alembic revision --autogenerate -m "create table"
    ```
  - upgrade the database
    ```bash
    alembic upgrade head # or alembic upgrade version_hash
    ```
  - downgrade the database
    ```bash
    alembic downgrade -1 # or alembic downgrade version_hash
    ```
- Optional step:
  ```bash
  pre-commit # install pre-commit hooks.
  choco install make # install make with admin privileges on Windows.
  ```
