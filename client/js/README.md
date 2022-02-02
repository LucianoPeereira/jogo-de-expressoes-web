# Kheiron API


## Project setup

Create and activate a virtualenv:

```
$ python3 -m venv .venv
$ source .venv/bin/activate
```

Install Python requirements:

```
$ pip install -r requirements.txt
```

Configure the Django environment:

- Rename the sample environment file to `.env`:
    ```
    $ mv .env.example .env
    ```
- Edit the `.env` file and provide a value for `SECRET_KEY`


```
$ python manage.py makemigrations
$ python manage.py migrate
```

### Running the API locally

```
$ python manage.py runserver
```

The API is now running at http://localhost:8000