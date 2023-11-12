## Create a virtual enviroment

```sh
python3.8 -m venv env
```

## Access the virtual enviroment

```sh
source env/bin/activate
```

## Install dependencies

```sh
pip install -r requirements.txt
```

## Run the Postgresql database container

```sh
pip docker-compose up -d db
```

## Aply all migrations to your database

```sh
python3 manage.py migrate
```

## Run the project

```sh
python3 manage.py runserver
```
