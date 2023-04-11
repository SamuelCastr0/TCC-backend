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

## Create a Postgresql database

You'll need to create a database with Postgresql, follow this tutorial if you need help.  
https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-20-04

## Setup your database in the application

After creating the database you must go to "/TCC/settings.py" and changes the DATABASE config according to what you created

Exemple:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tcc',
        'USER': 'admin',
        'PASSWORD': 'postgresql',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```

## Aply all migrations to your database

```sh
python3 manage.py migrate
```

## Run the project

```sh
python3 manage.py runserver
```
