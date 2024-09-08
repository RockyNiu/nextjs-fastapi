# backend

- install
  ```bash
  pip install poetry # install poetry.
  poetry shell # activate virtual environment, if not already activated.
  poetry install # install dependencies.
  ```
- in `config` directory, create a .secrets.test.toml file and a .secrets.development.toml file with the following content:
  ```toml
  dynaconf_merge = true

  [MYSQL]
  username = "user"
  password = "password"
  ```
- Optional step:
  ```bash
  pre-commit # install pre-commit hooks.
  choco install make # install make with admin privileges on Windows.
  ```