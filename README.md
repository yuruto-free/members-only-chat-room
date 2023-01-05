# MembersOnly Chat Room
## Preparation
1. Run the following command to install `pipenv` command.

    ```bash
    pip install pipenv
    ```

1. Execute the following command to install the dependent libraries.

    ```bash
    pipenv install
    ```

1. Create the `.env` file with reference to the following format.

    ```bash
    DJANGO_SECRET_KEY=abcdefghijklmnopqrstuvwxyz0123456789
    DJANGO_SUPERUSER_NAME=superuser
    DJANGO_SUPERUSER_EMAIL=superuser@local.jp
    DJANGO_SUPERUSER_PASSWORD=superuserpassword
    ```

1. Run the following command.

    ```bash
    cd src
    # migrate
    pipenv run python3 manage.py makemigrations
    pipenv run python3 manage.py migrate
    # create superuser account
    pipenv run python3 manage.py createsuperuser --noinput
    ```

## Execution
Execute the following command, then access the `http://localhost:8000`.

```bash
cd src
pipenv run daphne -b 0.0.0.0 -p 8000 config.asgi:application
```